"""
KOSGEB program oto-güncelleme servisi (derin çekim).

Akış:
  1. Destekler listeleme sayfasını çek → TÜM program detay linklerini çıkar.
  2. Her detay sayfasına gir → Groq ile yapısal çıkar (amaç, şartlar, destek
     unsurları: tutar/oran/süre, kriterler, varsa tarihler).
  3. DB ile karşılaştır → SADECE `ProgramUpdateProposal` (onay bekleyen öneri)
     oluştur. Canlı `kosgeb_programs` tablosuna ASLA dokunmaz.
  4. DB'de olup KOSGEB'de artık listelenmeyen aktif programlar için "deactivate"
     (kaldırma) önerisi üret — admin onaylarsa pasife alınır.

Her hata `ProgramFetchLog`'a yazılır; canlı site asla bozulmaz.
"""
import json
import re
import html as html_lib
from datetime import date

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import KosgebProgram, ProgramUpdateProposal, ProgramFetchLog
from app.services.ai_generator import llm_complete  # sıralı fallback'lı LLM motoru

# KOSGEB destekler listeleme sayfası (detay linkleri buradan toplanır)
LISTING_URL = "https://www.kosgeb.gov.tr/site/tr/genel/destekler/3/destekler"
_BASE = "https://www.kosgeb.gov.tr"

# Detay sayfası link kalıbı: /site/tr/genel/destekdetay/9327/sektorel-...-programi
_DETAIL_RE = re.compile(r"/site/tr/genel/destekdetay/(\d+)/([a-z0-9\-]+)", re.IGNORECASE)

_MAX_DETAILS = 20         # tek taramada en fazla detay sayfası (güvenlik sınırı)
_MAX_RAW = 30_000         # AI'ya gönderilen metin üst sınırı
_MIN_HEALTHY = 3          # kaldırma önerisi üretmek için gereken min. başarılı program

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

# proposed_data içinde tutulacak alanlar (DB ile diff'lenen)
_FIELDS = [
    "program_name", "program_code", "max_support_amount", "support_type",
    "min_business_age_months", "max_business_age_months",
    "application_period_start", "application_period_end",
    "required_documents", "key_criteria",
    "purpose", "eligibility", "support_items", "detail_url",
]


def _strip_html(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    text = re.sub(r"(?s)<[^>]+>", " ", raw)
    text = html_lib.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


async def _fetch_raw(url: str) -> tuple[int | None, str | None, str | None]:
    """Ham HTML döndürür (status, html, error)."""
    try:
        async with httpx.AsyncClient(timeout=25, follow_redirects=True,
                                     headers={"User-Agent": _USER_AGENT}) as ac:
            resp = await ac.get(url)
            if resp.status_code != 200:
                return resp.status_code, None, f"HTTP {resp.status_code}"
            return resp.status_code, resp.text, None
    except Exception as e:
        return None, None, str(e)[:300]


def _extract_detail_links(html: str) -> list[tuple[str, str]]:
    """Listeleme HTML'inden (detay_url, kod) çiftlerini çıkar. Dedup'lu, sırayı korur."""
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for m in _DETAIL_RE.finditer(html):
        pid = m.group(1)
        if pid in seen:
            continue
        seen.add(pid)
        path = m.group(0)
        out.append((_BASE + path, f"K{pid}"))
    return out


_DETAIL_PROMPT = """Aşağıdaki metin TEK bir KOSGEB destek programının resmi sayfasıdır. İçerikten program bilgilerini çıkar.

SADECE ve SADECE tek bir JSON NESNESİ döndür. Başka açıklama yazma. Bilinmeyen alanı null bırak:
{{
  "program_name": "programın tam resmi adı",
  "support_type": "hibe | kredi_faiz | karma | geri_odemeli",
  "max_support_amount": en yüksek azami destek tutarı (sadece tam sayı TL, örn. 14000000) veya null,
  "purpose": "programın amacı/tanımı, 2-4 cümlelik akıcı Türkçe özet",
  "eligibility": "kimler başvurabilir ve temel başvuru şartları; kısa, madde madde düz metin",
  "support_items": [
    {{"unsur": "destek unsuru adı", "tutar": "üst limit (örn. 6.506.000 TL) veya boş", "oran": "destek oranı (örn. %60) veya boş", "sure": "destek süresi (örn. 10 Yıl) veya boş"}}
  ],
  "key_criteria": ["en önemli 3-6 kriter"],
  "required_documents": ["başvuru için gereken belgeler"] veya null,
  "application_period_start": "YYYY-MM-DD" veya null,
  "application_period_end": "YYYY-MM-DD" veya null
}}

ÖNEMLİ:
- Tarih (başvuru başlangıç/bitiş) KESİN ve net olarak belirtilmemişse null bırak. Tahmin etme.
- "Destek Unsurları" tablosundaki her satırı support_items içine ekle (tutar/oran/süre ile).
- SADECE Türkçe yaz, başka alfabe kullanma.

Metin:
{text}
"""


async def _ai_parse_detail(text: str, fallback_code: str) -> dict | None:
    """Tek bir detay sayfası metnini yapısal program dict'ine çevirir."""
    try:
        out = (await llm_complete(
            [{"role": "user", "content": _DETAIL_PROMPT.format(text=text)}],
            temperature=0.1, max_tokens=2000, rounds=2,
        )).strip()
        if out.startswith("```"):
            out = re.sub(r"^```(?:json)?|```$", "", out).strip()
        data = json.loads(out)
        if not isinstance(data, dict):
            return None
        return data
    except Exception:
        return None


def _normalize(item: dict, detail_url: str, code: str) -> dict | None:
    """AI çıktısını KosgebProgram alanlarına normalize et; geçersizse None."""
    name = (item.get("program_name") or "").strip()
    if not name:
        return None
    out = {f: item.get(f) for f in _FIELDS}
    out["program_name"] = name
    out["program_code"] = (item.get("program_code") or code)
    out["detail_url"] = detail_url

    # Tarihleri doğrula (ISO string olarak sakla; geçersizse null)
    for dk in ("application_period_start", "application_period_end"):
        v = out.get(dk)
        if v:
            try:
                date.fromisoformat(str(v))
            except Exception:
                out[dk] = None

    # max_support_amount int'e zorla
    if out.get("max_support_amount") is not None:
        try:
            out["max_support_amount"] = int(out["max_support_amount"])
        except Exception:
            out["max_support_amount"] = None

    # support_items düzgün liste mi?
    si = out.get("support_items")
    if not isinstance(si, list):
        out["support_items"] = None
    return out


def _program_to_dict(p: KosgebProgram) -> dict:
    return {
        "program_name": p.program_name,
        "program_code": p.program_code,
        "max_support_amount": p.max_support_amount,
        "support_type": p.support_type,
        "min_business_age_months": p.min_business_age_months,
        "max_business_age_months": p.max_business_age_months,
        "application_period_start": p.application_period_start.isoformat() if p.application_period_start else None,
        "application_period_end": p.application_period_end.isoformat() if p.application_period_end else None,
        "required_documents": list(p.required_documents) if p.required_documents else None,
        "key_criteria": list(p.key_criteria) if p.key_criteria else None,
        "purpose": p.purpose,
        "eligibility": p.eligibility,
        "support_items": p.support_items,
        "detail_url": p.detail_url,
    }


def _diff(current: dict, proposed: dict) -> list[dict]:
    changes = []
    for f in _FIELDS:
        old, new = current.get(f), proposed.get(f)
        if new is not None and new != old:
            changes.append({"field": f, "old": old, "new": new})
    return changes


async def run_scrape(db: AsyncSession, triggered_by: str = "schedule") -> dict:
    """Tüm programları derinlemesine işle, öneriler üret. Hatalar canlıya yansımaz."""
    total_proposals = 0
    logs: list[dict] = []

    # Mevcut programları indeksle
    existing_res = await db.execute(select(KosgebProgram))
    existing = existing_res.scalars().all()
    by_code = {p.program_code: p for p in existing if p.program_code}
    by_name = {p.program_name.lower(): p for p in existing}

    # 1) Listeleme sayfası → detay linkleri
    http_status, listing_html, error = await _fetch_raw(LISTING_URL)
    if error or not listing_html:
        db.add(ProgramFetchLog(source_url=LISTING_URL, status="fetch_failed",
                               http_status=http_status, error=error, triggered_by=triggered_by))
        await db.commit()
        return {"total_proposals": 0, "sources": [{"url": LISTING_URL, "status": "fetch_failed", "error": error}]}

    links = _extract_detail_links(listing_html)[:_MAX_DETAILS]
    fetch_log = ProgramFetchLog(source_url=LISTING_URL, status="success",
                                http_status=http_status, raw_text=f"{len(links)} program linki bulundu",
                                triggered_by=triggered_by)
    db.add(fetch_log)
    await db.flush()  # fetch_log.id

    seen_codes: set[str] = set()
    parsed_ok = 0

    # 2) Her detay sayfasını işle
    for detail_url, code in links:
        d_status, d_html, d_err = await _fetch_raw(detail_url)
        if d_err or not d_html:
            logs.append({"url": detail_url, "status": "fetch_failed", "error": d_err})
            continue

        text = _strip_html(d_html)[:_MAX_RAW]
        raw_item = await _ai_parse_detail(text, code)
        if not raw_item:
            logs.append({"url": detail_url, "status": "parse_failed"})
            continue

        item = _normalize(raw_item, detail_url, code)
        if not item:
            logs.append({"url": detail_url, "status": "empty"})
            continue

        parsed_ok += 1
        seen_codes.add(item["program_code"])

        match = by_code.get(item["program_code"]) or by_name.get(item["program_name"].lower())
        if match:
            current = _program_to_dict(match)
            changes = _diff(current, item)
            if not changes:
                logs.append({"url": detail_url, "status": "no_change", "program": item["program_name"]})
                continue
            change_type, program_id, current_data = "update", match.id, current
        else:
            change_type, program_id, current_data, changes = "create", None, None, None

        # Aynı bekleyen öneri var mı? (de-dupe; eskisini supersede et)
        dup_res = await db.execute(
            select(ProgramUpdateProposal).where(
                ProgramUpdateProposal.status == "pending",
                ProgramUpdateProposal.program_code == item["program_code"],
                ProgramUpdateProposal.change_type == change_type,
            )
        )
        is_dup = False
        for d in dup_res.scalars().all():
            if d.proposed_data == item:
                is_dup = True
            else:
                d.status = "superseded"
        if is_dup:
            logs.append({"url": detail_url, "status": "duplicate", "program": item["program_name"]})
            continue

        db.add(ProgramUpdateProposal(
            program_id=program_id,
            program_code=item["program_code"],
            change_type=change_type,
            proposed_data=item,
            current_data=current_data,
            diff_summary={"changes": changes} if changes else None,
            source_url=detail_url,
            raw_excerpt=text[:1500],
            confidence="medium",
            status="pending",
            fetch_log_id=fetch_log.id,
        ))
        total_proposals += 1
        logs.append({"url": detail_url, "status": change_type, "program": item["program_name"]})

    # 3) KOSGEB'de artık listelenmeyen aktif programlar için kaldırma önerisi
    #    (yalnızca tarama sağlıklıysa — kısmi hatada toplu kaldırma yapma)
    removals = 0
    if parsed_ok >= _MIN_HEALTHY:
        for p in existing:
            if not p.is_active:
                continue
            if p.program_code in seen_codes:
                continue
            # Zaten bekleyen kaldırma önerisi var mı?
            dup = await db.execute(
                select(ProgramUpdateProposal).where(
                    ProgramUpdateProposal.status == "pending",
                    ProgramUpdateProposal.program_id == p.id,
                    ProgramUpdateProposal.change_type == "deactivate",
                )
            )
            if dup.scalar_one_or_none():
                continue
            db.add(ProgramUpdateProposal(
                program_id=p.id,
                program_code=p.program_code,
                change_type="deactivate",
                proposed_data={"is_active": False},
                current_data=_program_to_dict(p),
                diff_summary={"note": "Bu program KOSGEB destekler sayfasında artık listelenmiyor; kaldırılması (pasife alınması) öneriliyor."},
                source_url=LISTING_URL,
                confidence="medium",
                status="pending",
                fetch_log_id=fetch_log.id,
            ))
            removals += 1
            total_proposals += 1

    fetch_log.proposals_created = total_proposals
    if total_proposals == 0:
        fetch_log.status = "no_change"

    await db.commit()
    return {
        "total_proposals": total_proposals,
        "programs_found": parsed_ok,
        "removals_proposed": removals,
        "sources": logs,
    }
