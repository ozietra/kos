"""
KOSGEB program oto-güncelleme servisi.

Akış: kosgeb.gov.tr'den çek → Groq ile yapısal ayrıştır → DB ile karşılaştır →
SADECE `ProgramUpdateProposal` (onay bekleyen öneri) oluştur. Canlı
`kosgeb_programs` tablosuna ASLA dokunmaz; değişiklik yalnızca admin onayıyla
uygulanır. Her hata `ProgramFetchLog`'a yazılır, canlı site asla bozulmaz.
"""
import json
import re
import html as html_lib
from datetime import date

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import KosgebProgram, ProgramUpdateProposal, ProgramFetchLog
from app.services.ai_generator import client  # mevcut AsyncGroq istemcisi

# Çekilecek KOSGEB kaynak sayfaları (gerektikçe genişletilebilir)
SOURCE_URLS = [
    "https://www.kosgeb.gov.tr/site/tr/genel/destekler/3/destekler",
]

_MAX_RAW = 45_000
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

# proposed_data içinde tutulacak alanlar
_FIELDS = [
    "program_name", "program_code", "max_support_amount", "support_type",
    "eligible_nace_prefixes", "min_business_age_months", "max_business_age_months",
    "application_period_start", "application_period_end",
    "required_documents", "key_criteria",
]


def _strip_html(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    text = re.sub(r"(?s)<[^>]+>", " ", raw)
    text = html_lib.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


async def _fetch(url: str) -> tuple[int | None, str | None, str | None]:
    try:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True,
                                     headers={"User-Agent": _USER_AGENT}) as ac:
            resp = await ac.get(url)
            if resp.status_code != 200:
                return resp.status_code, None, f"HTTP {resp.status_code}"
            return resp.status_code, _strip_html(resp.text)[:_MAX_RAW], None
    except Exception as e:
        return None, None, str(e)[:300]


_PARSE_PROMPT = """Aşağıdaki metin KOSGEB destek programları hakkındadır. Metinden program bilgilerini çıkar.

SADECE ve SADECE bir JSON DİZİSİ döndür. Başka açıklama yazma. Her öğe şu alanları içersin (bilinmiyorsa null bırak):
[
  {{
    "program_name": "tam program adı",
    "program_code": "kısa kod (örn. IGD-2026) veya null",
    "max_support_amount": tam sayı TL (örn. 2000000) veya null,
    "support_type": "hibe | kredi_faiz | karma | geri_odemeli",
    "min_business_age_months": tam sayı veya null,
    "max_business_age_months": tam sayı veya null,
    "application_period_start": "YYYY-MM-DD" veya null,
    "application_period_end": "YYYY-MM-DD" veya null,
    "required_documents": ["belge1", "belge2"],
    "key_criteria": ["kriter1", "kriter2"]
  }}
]

Metin:
{text}
"""


async def _ai_parse(text: str) -> list[dict] | None:
    try:
        resp = await client.chat.completions.create(
            messages=[{"role": "user", "content": _PARSE_PROMPT.format(text=text)}],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=2500,
        )
        out = resp.choices[0].message.content.strip()
        if out.startswith("```"):
            out = re.sub(r"^```(?:json)?|```$", "", out).strip()
        data = json.loads(out)
        return data if isinstance(data, list) else None
    except Exception:
        return None


def _normalize(item: dict) -> dict | None:
    """AI öğesini KosgebProgram alanlarına normalize et; geçersizse None."""
    name = (item.get("program_name") or "").strip()
    if not name:
        return None
    out = {f: item.get(f) for f in _FIELDS}
    out["program_name"] = name
    # Tarihleri doğrula (ISO string olarak sakla)
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
    return out


def _program_to_dict(p: KosgebProgram) -> dict:
    return {
        "program_name": p.program_name,
        "program_code": p.program_code,
        "max_support_amount": p.max_support_amount,
        "support_type": p.support_type,
        "eligible_nace_prefixes": list(p.eligible_nace_prefixes) if p.eligible_nace_prefixes else None,
        "min_business_age_months": p.min_business_age_months,
        "max_business_age_months": p.max_business_age_months,
        "application_period_start": p.application_period_start.isoformat() if p.application_period_start else None,
        "application_period_end": p.application_period_end.isoformat() if p.application_period_end else None,
        "required_documents": list(p.required_documents) if p.required_documents else None,
        "key_criteria": list(p.key_criteria) if p.key_criteria else None,
    }


def _diff(current: dict, proposed: dict) -> list[dict]:
    changes = []
    for f in _FIELDS:
        old, new = current.get(f), proposed.get(f)
        if new is not None and new != old:
            changes.append({"field": f, "old": old, "new": new})
    return changes


async def run_scrape(db: AsyncSession, triggered_by: str = "schedule") -> dict:
    """Tüm kaynakları işle, öneriler üret. Hatalar canlıya yansımaz."""
    total_proposals = 0
    logs = []

    # Mevcut programları kod ve isme göre indeksle
    existing_res = await db.execute(select(KosgebProgram))
    existing = existing_res.scalars().all()
    by_code = {p.program_code: p for p in existing if p.program_code}
    by_name = {p.program_name.lower(): p for p in existing}

    for url in SOURCE_URLS:
        http_status, text, error = await _fetch(url)
        if error or not text:
            db.add(ProgramFetchLog(source_url=url, status="fetch_failed",
                                   http_status=http_status, error=error,
                                   triggered_by=triggered_by))
            logs.append({"url": url, "status": "fetch_failed", "error": error})
            continue

        parsed = await _ai_parse(text)
        if parsed is None:
            db.add(ProgramFetchLog(source_url=url, status="parse_failed",
                                   http_status=http_status, raw_text=text,
                                   error="AI ayrıştırma başarısız", triggered_by=triggered_by))
            logs.append({"url": url, "status": "parse_failed"})
            continue

        created_here = 0
        fetch_log = ProgramFetchLog(source_url=url, status="success",
                                    http_status=http_status, raw_text=text,
                                    triggered_by=triggered_by)
        db.add(fetch_log)
        await db.flush()  # fetch_log.id

        for raw_item in parsed:
            item = _normalize(raw_item)
            if not item:
                continue
            match = by_code.get(item.get("program_code")) or by_name.get(item["program_name"].lower())

            if match:
                current = _program_to_dict(match)
                changes = _diff(current, item)
                if not changes:
                    continue
                change_type, program_id, current_data = "update", match.id, current
            else:
                change_type, program_id, current_data, changes = "create", None, None, None

            # Aynı bekleyen öneri var mı? (basit de-dupe)
            dup_res = await db.execute(
                select(ProgramUpdateProposal).where(
                    ProgramUpdateProposal.status == "pending",
                    ProgramUpdateProposal.program_code == item.get("program_code"),
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
                continue

            db.add(ProgramUpdateProposal(
                program_id=program_id,
                program_code=item.get("program_code"),
                change_type=change_type,
                proposed_data=item,
                current_data=current_data,
                diff_summary={"changes": changes} if changes else None,
                source_url=url,
                raw_excerpt=text[:1500],
                confidence="medium",
                status="pending",
                fetch_log_id=fetch_log.id,
            ))
            created_here += 1
            total_proposals += 1

        fetch_log.proposals_created = created_here
        if created_here == 0:
            fetch_log.status = "no_change"
        logs.append({"url": url, "status": fetch_log.status, "proposals": created_here})

    await db.commit()
    return {"total_proposals": total_proposals, "sources": logs}
