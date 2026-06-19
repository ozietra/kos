"""
AI Başvuru Metni Üretici — Groq Llama-3 Altyapısı (Faz 6)
Kademeli üretim (Chunking) ve %90 Başarı (Self-Correction) filtreli
"""
import os
import re
import asyncio
import logging
from datetime import date
from typing import AsyncGenerator
from openai import AsyncOpenAI
from app.config import settings

logger = logging.getLogger("kosgeb.ai")

# ─── METIN TEMIZLEME (yabanci alfabe temizleyici) ──────────
# Llama modeli, Turkce yazmasi istense de ara sira farkli alfabelerden karakter
# (Cince, Japonca, Korece, Kiril, Arapca vb.) sizdirabiliyor. Uretilen metni
# Latin/Turkce + ortak noktalama + para birimi disindaki karakterlerden arindirir.
# Araliklar kod noktasi olarak yazilir (kaynak ASCII kalsin diye chr ile kurulur):
#   0x0020-0x024F : Basic Latin + Latin-1 + Latin Ext-A/B (Turkce ozel harfler dahil)
#   0x2000-0x206F : Genel noktalama (tire, tirnak, ucnokta, madde imi)
#   0x20A0-0x20BF : Para birimi sembolleri (TL sembolu dahil)
_ALLOWED_RANGES = ((0x0020, 0x024F), (0x2000, 0x206F), (0x20A0, 0x20BF))
_NON_LATIN = re.compile(
    "[^" + "".join(chr(a) + "-" + chr(b) for a, b in _ALLOWED_RANGES) + r"\s]"
)


def _sanitize_tr(text: str) -> str:
    """Turkce/Latin disi karakterleri at, olusan cift bosluklari sadelestir."""
    if not text:
        return text
    text = _NON_LATIN.sub("", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r" +([,.;:!?])", r"\1", text)
    return text


# ─── YAPAY ZEKÂ SAĞLAYICILARI (sıralı fallback) ──────────────────────────────
# Tümü OpenAI-uyumlu API; tümü Llama-3.3-70B sunar. Sırayla denenir: biri limit
# (429) veya hata verince otomatik bir sonrakine geçilir. Hepsi dolduysa kısa
# bekleyip baştan dener. .env'e ne kadar çok anahtar koyarsan o kadar kapasite.
_PROVIDER_DEFS = [
    ("groq",       "https://api.groq.com/openai/v1", settings.GROQ_API_KEY,        settings.GROQ_MODEL),
    ("openrouter", "https://openrouter.ai/api/v1",   settings.OPENROUTER_API_KEY,  settings.OPENROUTER_MODEL),
    ("cerebras",   "https://api.cerebras.ai/v1",     settings.CEREBRAS_API_KEY,    settings.CEREBRAS_MODEL),
    ("together",   "https://api.together.xyz/v1",    settings.TOGETHER_API_KEY,    settings.TOGETHER_MODEL),
]


def _build_providers() -> list[dict]:
    provs: list[dict] = []
    # Birincil + ek Groq anahtarları (aynı/farklı hesaplar) — kapasiteyi katlar
    groq_keys = [settings.GROQ_API_KEY] + [
        k.strip() for k in (settings.GROQ_API_KEYS_EXTRA or "").split(",")
    ]
    for i, key in enumerate(dict.fromkeys([k for k in groq_keys if k])):  # benzersiz, dolu
        provs.append({
            "name": f"groq#{i + 1}",
            "client": AsyncOpenAI(base_url="https://api.groq.com/openai/v1", api_key=key, timeout=60.0),
            "model": settings.GROQ_MODEL,
        })
    # Diğer sağlayıcılar (yalnızca anahtarı doluysa)
    for name, base_url, key, model in _PROVIDER_DEFS[1:]:
        if key:
            provs.append({
                "name": name,
                "client": AsyncOpenAI(base_url=base_url, api_key=key, timeout=60.0),
                "model": model,
            })
    return provs


_PROVIDERS = _build_providers()

# ─── SİSTEM PROMPTU (Dinamik tarih) ──────────────────────────────────────────

_TR_MONTHS = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
              "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


def _current_period() -> str:
    t = date.today()
    return f"{_TR_MONTHS[t.month]} {t.year}"


SYSTEM_PROMPT = f"""Sen, KOBİ'ler için KOSGEB destek başvuru dosyaları hazırlayan, alanında uzman, deneyimli bir proje danışmanısın. {_current_period()} itibarıyla güncel KOSGEB değerlendirme kriterlerine hâkimsin.

KOSGEB değerlendirme jürisinin beklentileri:
- Gerçekçi, ölçülebilir, sayısal verilerle desteklenmiş somut hedefler. Afaki/abartılı rakamlar elenir.
- Dijital dönüşüm, yeşil/temiz enerji, yerli üretim ve ihracat odaklı projelere öncelik.
- Her bütçe kalemi ve her talep, mantıklı bir gerekçeyle ("neden gerekli, neye yarayacak, geri dönüşü ne") açıklanmalı.
- Yatırımın istihdama, üretime ve ülke ekonomisine katkısı net ortaya konmalı.

EN KRİTİK KURAL — VERİ SADAKATİ:
- Başvuru sahibinin verdiği rakamlara (bütçe kalemleri ve tutarları, toplam talep, ilk yıl gelir hedefi, istihdam sayısı, proje süresi) MUTLAK sadık kal. Bu rakamları AYNEN kullan.
- ASLA kendi kafandan farklı bir rakam UYDURMA, yuvarlama veya değiştirme. Örneğin talep 200.000 TL ise hiçbir yerde 500.000 TL yazma.
- Bölümler arası ÇELİŞME yasak: bir bölümde gelir 1.000.000 TL diyip başka bölümde 5.000.000 TL deme. Tüm dosyada aynı rakamlar geçer.
- Bütçe kalemleri verilenlerdir (örn. donanım, yazılım, eğitim). Kendi kafandan "kuruluş gideri, personel gideri, makine-teçhizat" gibi kalemler EKLEME.
- Bilgi verilmemişse uydurma; o noktayı genel ama tutarlı biçimde geç.

TEKRAR YASAĞI:
- Aynı cümleyi, fikri veya kalıbı tekrarlama. Her cümle yeni bir bilgi/argüman katmalı.
- "KOSGEB tarafından desteklenen sektörlerde faaliyet göstererek sürdürülebilirliğini sağlamak" gibi içi boş, döngüsel dolgu cümleleri yazma.

EN YÜKSEK ONAY İHTİMALİ:
- Verilen bilgilerden hareketle, jürinin onaylama ihtimali en yüksek, somut ve gerçekçi senaryoyu kur.
- Soyut vaatler yerine ölçülebilir hedef + gerekçe + beklenen sonuç üçlüsünü kullan.

YAZIM KURALLARI:
- Doğrudan dosya metnini yaz. "Tabii ki", "Kesinlikle", "Anlaşıldı", "İşte metniniz", "Umarım yardımcı olur" gibi sohbet/asistan kalıplarını ASLA kullanma.
- Profesyonel bir danışmanın ağzından, resmi ama akıcı, ikna edici ve özgüvenli bir Türkçe kullan.
- SADECE TÜRKÇE yaz. Hiçbir yabancı dil kelimesi, farklı alfabe veya bozuk/uydurma kelime (örn. "tăngırmak") kullanma. Şüpheye düşersen yaygın, doğru Türkçe kelimeyi seç.
- Hiçbir platform, marka, web sitesi veya yazılım adı geçirme. Metin, danışmanın işletme adına bizzat hazırladığı bir dosya gibi olmalı.
- "Gerekçe → Sonuç" mantığıyla, jüriyi ikna edecek ciddiyette yaz.
"""

# ─── YARDIMCI FONKSİYONLAR ──────────────────────────────────────────────────

def _is_rate_limit(err_str: str) -> bool:
    return any(k in err_str for k in ("429", "rate limit", "rate_limit", "resource_exhausted", "too many requests"))


def _retry_after_seconds(err_str: str, attempt: int) -> float:
    """Groq hata metni 'try again in 12.3s' içerebilir; yoksa artan bekleme."""
    m = re.search(r"try again in ([\d.]+)\s*s", err_str)
    if m:
        try:
            return min(float(m.group(1)) + 1.0, 35.0)
        except Exception:
            pass
    return min(6.0 * (attempt + 1), 30.0)  # 6, 12, 18, 24, 30...


async def llm_complete(
    messages: list[dict],
    temperature: float = 0.6,
    max_tokens: int = 1800,
    rounds: int = 3,
) -> str:
    """Sağlayıcıları SIRAYLA dener. Biri limit/hata verince hemen sonrakine geçer.
    Bir turda hepsi başarısız olursa (örn. hepsi limitte) kısa bekleyip baştan
    dener — `rounds` kadar. Ham metni döndürür (temizleme çağırana ait)."""
    if not _PROVIDERS:
        raise Exception("Yapay zekâ sağlayıcısı yapılandırılmamış. Lütfen .env içine en az bir GROQ_API_KEY ekleyin.")

    last_err: Exception | None = None
    for rnd in range(rounds):
        all_rate_limited = True
        for prov in _PROVIDERS:
            try:
                resp = await prov["client"].chat.completions.create(
                    messages=messages,
                    model=prov["model"],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                content = (resp.choices[0].message.content or "").strip()
                if content:
                    return content
                all_rate_limited = False  # boş yanıt; limit değil
            except Exception as e:
                last_err = e
                if not _is_rate_limit(str(e).lower()):
                    all_rate_limited = False
                logger.warning("LLM sağlayıcı '%s' başarısız (tur %d): %s", prov["name"], rnd + 1, str(e)[:160])
                continue  # bir sonraki sağlayıcıyı dene
        # Tüm sağlayıcılar bu turda başarısız oldu
        if all_rate_limited and rnd < rounds - 1:
            await asyncio.sleep(_retry_after_seconds(str(last_err or "").lower(), rnd))
        elif rnd < rounds - 1:
            await asyncio.sleep(2.0)  # geçici hata; kısa bekle, tekrar dene
    raise Exception("Analiz sunucularımızda anlık bir yoğunluk yaşanıyor. Lütfen işleminizi 1-2 dakika sonra tekrar deneyiniz.")


async def call_groq(prompt: str, max_tokens: int = 1800, rounds: int = 3) -> str:
    """Sistem promptu + kullanıcı promptu ile üretim yapar; çıktıyı temizler."""
    content = await llm_complete(
        [{"role": "system", "content": SYSTEM_PROMPT},
         {"role": "user", "content": prompt}],
        temperature=0.4, max_tokens=max_tokens, rounds=rounds,
    )
    return _sanitize_tr(content)


async def evaluate_and_improve(text: str, context_prompt: str) -> str:
    """
    Self-Correction mekanizması:
    Üretilen metne 100 üzerinden puan verir. 90'ın altındaysa iyileştirip döndürür.
    """
    eval_prompt = f"""Aşağıdaki metin bir KOSGEB başvuru dokümanı için yazıldı.
İlgili Bağlam/Görev: {context_prompt}

Değerlendirme Kriterleri (güncel KOSGEB standartları):
1. Afaki, ölçülemez, soyut ifadeler var mı?
2. Bütçe, istihdam veya pazar hedefleri mantıklı ve destekli mi?
3. Yapay zeka kalıpları (Tabii ki, Kesinlikle vb.) kullanılmış mı?
4. KOSGEB uzmanının onayını %90 ihtimalle alacak ciddiyette mi?

Görev:
Eğer bu metin 100 üzerinden 90 ve üzeri puan almayı hak ediyorsa, sadece "<APPROVED>" yaz.
Eğer puan 90'ın altındaysa, metindeki hataları/eksikleri düzelterek YEPYENİ, MÜKEMMEL versiyonunu yaz. (Ek açıklama yapma, sadece yeni mükemmel metni ver).

İncelenecek Metin:
{text}
    """
    # Bu adım OPSİYONEL kalite kontrolüdür; hız limiti vb. ile başarısız olursa
    # üretimi düşürmek yerine orijinal taslağı koru (kısa, tek-iki deneme).
    try:
        eval_response = await call_groq(eval_prompt, rounds=1)
    except Exception:
        return text
    if "<APPROVED>" in eval_response.upper():
        return text
    
    # Yeni metin üretildi, temizle ve döndür (boş gelirse orijinali koru)
    return eval_response.replace("<APPROVED>", "").strip() or text


def build_prompt(template: str, inputs: dict) -> str:
    from string import Formatter
    keys = [fname for _, fname, _, _ in Formatter().parse(template) if fname]
    fill = {k: inputs.get(k) or "belirtilmemiş" for k in keys}
    body = template.format(**fill)
    # Başvurulan programın gerçek bilgileri varsa, her bölümün başına ekle ki
    # metin o programın amacı/şartları/destek unsurlarına birebir uygun yazılsın.
    prefix_parts: list[str] = []
    # 1) Başvuru sahibinin girdiği KESİN bilgiler (rakamlar) — en yüksek öncelik
    facts = (inputs.get("facts_block") or "").strip()
    if facts:
        prefix_parts.append(
            "BAŞVURU SAHİBİNİN GİRDİĞİ KESİN BİLGİLER — Bu rakam ve verileri AYNEN kullan; "
            "ASLA farklı/uydurma rakam (bütçe, gelir, istihdam, süre) verme ve bu verilerle ÇELİŞME:\n"
            f"{facts}"
        )
    # 2) Başvurulan programın resmi bilgileri (varsa)
    ctx = (inputs.get("program_context") or "").strip()
    if ctx:
        prefix_parts.append(
            "BAŞVURULAN KOSGEB PROGRAMININ RESMİ BİLGİLERİ "
            "(metni bu programın amacı, başvuru şartları ve destek unsurlarına uygun, bunlara atıfla yaz):\n"
            f"{ctx}"
        )
    if prefix_parts:
        return "\n\n".join(prefix_parts) + "\n\n---\n" + body
    return body


# ─── SEKSİYON FONKSİYONLARI ──────────────────────────────────────────────────

PROJECT_SUMMARY_PROMPT = """Aşağıdaki bilgilere göre KOSGEB İş Geliştirme Desteği için 400-600 kelimelik "Proje Özeti" yaz.

 İŞLETME: {business_name} | NACE: {nace_code} | Şehir: {city} | Yaş: {business_age_months} ay
 ÖZEL KATEGORİ: {special_category}
 PROJE FİKRİ: {project_idea}
 ÇÖZÜLEN PROBLEM: {problem_solved}
 BÜTÇE/TALEP: {requested_amount} TL → Kalemler: {budget_items}
 İSTİHDAM/GELİR: {employment_target} kişi, {revenue_target_year1} TL ilk yıl geliri.

 Doğrudan özeti yaz, başlık atma.
"""

async def generate_project_summary(inputs: dict) -> str:
    prompt = build_prompt(PROJECT_SUMMARY_PROMPT, inputs)
    draft = await call_groq(prompt)
    return await evaluate_and_improve(draft, "Proje Özeti")


BUSINESS_PLAN_CHUNKS = [
    ("Pazar Analizi ve Değer Önerisi", """
İşletme: {business_name} | NACE: {nace_code} | Hedef Kitle: {target_market} | Rekabet Avantajı: {competitive_advantage}
Bu bilgilere göre KOSGEB İş Planının "Pazar Analizi" ve "Değer Önerisi" kısımlarını yaz. 
400 kelime civarı olsun. Akıcı ve bürokratik bir dil kullan. Başlıkları Markdown olarak at.
    """),
    
    ("İş Modeli ve Pazarlama", """
İşletme: {business_name} | NACE: {nace_code} | Hedef Kitle: {target_market} | Gelir Hedefi: {revenue_target_year1} TL
Bu bilgilere göre KOSGEB İş Planının "İş Modeli" ve "Pazarlama ve Satış Stratejisi" kısımlarını yaz.
400 kelime civarı olsun. Gerçekçi pazarlama yöntemlerini anlat. Başlıkları Markdown olarak at.
    """),
    
    ("Operasyonel Plan ve Riskler", """
İşletme: {business_name} | NACE: {nace_code} | Proje: {project_title}
Bu bilgilere göre KOSGEB İş Planının "Operasyonel Plan" ve "Riskler ve Önlemler (3 ana risk)" kısımlarını yaz.
400 kelime civarı olsun. Operasyon adımlarını mantıklı kur. Başlıkları Markdown olarak at.
    """)
]

async def generate_business_plan_chunked(inputs: dict) -> AsyncGenerator[tuple[str, str], None]:
    """Her parçayı ayrı üreterek limite takılmadan birleştirir. Tuple(section_name, content) döndürür."""
    for name, template in BUSINESS_PLAN_CHUNKS:
        prompt = build_prompt(template, inputs)
        draft = await call_groq(prompt)
        final_text = await evaluate_and_improve(draft, f"İş Planı - {name}")
        yield (name, final_text)


FINANCIAL_PROJECTION_PROMPT = """
Aşağıdaki finansal bilgilere dayanarak 3 yıllık finansal projeksiyonun neden gerçekçi olduğunu MÜŞTERİ VEYA KOSGEB JÜRİSİ GÖZÜNDEN açıklayan profesyonel bir metin yaz.
Bütçe kalemleri: {budget_items}
Toplam talep: {requested_amount} TL
1. yıl gelir hedefi: {revenue_target_year1} TL
İstihdam: {employment_target} kişi
Sektör: {nace_code} - {nace_description}

Somut gerekçeler, maliyet analizleri, ve yatırımın KOSGEB'e (Türkiye'ye) dönüşü/katkısı (ROI) üzerinden açıklama yap. Ortalama 300 kelime. Tablo değil, metin ver.
"""

async def generate_financial_projection(inputs: dict) -> str:
    prompt = build_prompt(FINANCIAL_PROJECTION_PROMPT, inputs)
    draft = await call_groq(prompt)
    return await evaluate_and_improve(draft, "Finansal Projeksiyon Argümantasyonu")


TIMELINE_PROMPT = """
Proje süresi: {project_duration_months} ay
Kilometre taşları: {milestones}
Proje başlığı: {project_title}
Bütçe kalemleri: {budget_items}

Her ay (veya 3 aylık dönemler) için ne yapılacağını mantıklı bir iş planı sırasıyla listele. İlk ay kurulum, orta aylar operasyon, son aylar pazarlama gibi.
Toplam 150-200 kelime. Liste formatında.
"""

async def generate_timeline(inputs: dict) -> str:
    prompt = build_prompt(TIMELINE_PROMPT, inputs)
    draft = await call_groq(prompt)
    return await evaluate_and_improve(draft, "Proje Zaman Çizelgesi")


# ─── BELGE KONTROL LİSTESİ ────────────────────────────────────────────────────

DOCUMENT_CHECKLIST = {
    "IGD": [  
        {"id": "ruhsat", "name": "İşyeri Açma ve Çalışma Ruhsatı", "description": "Belediyeden alınır.", "where_to_get": "İlçe Belediyesi", "required": True},
        {"id": "vergi_levhasi", "name": "Vergi Levhası", "description": "Güncel.", "where_to_get": "GİB İnteraktif", "required": True},
        {"id": "ticaret_sicil", "name": "Ticaret Sicil Gazetesi", "description": "Kuruluş gazetesi.", "where_to_get": "Ticaret Sicil", "required": True},
        {"id": "kosgeb_kayit", "name": "KOSGEB Veri Tabanı Kaydı", "description": "E-KOBİ.", "where_to_get": "KOSGEB Portal", "required": True},
        {"id": "proforma", "name": "Proforma Faturalar", "description": "Talep edilen 3 kalem için proforma.", "where_to_get": "Tedarikçiler", "required": True},
    ],
}

def generate_document_checklist(program_type: str) -> list[dict]:
    return DOCUMENT_CHECKLIST["IGD"]

# ─── NACE KODU ÖNERİSİ ────────────────────────────────────────────────────────

async def suggest_nace(description: str) -> dict:
    """Kullanıcının sektör açıklamasına göre NACE kodu önerir (Groq Llama-3 Tarafından)."""
    prompt = f"""Aşağıdaki iş fikrini analiz et ve en uygun KOSGEB NACE kodunu bul.
İş Fikri: {description}

LÜTFEN SADECE VE SADECE JSON FORMATINDA YANIT VER. BAŞKA HİÇBİR AÇIKLAMA VEYA METİN YAZMA.
{{
    "nace_code": "Örn: 62.01",
    "nace_description": "Örn: Bilgisayar programlama faaliyetleri",
    "is_kosgeb_eligible": true,
    "confidence": "high",
    "alternative_codes": ["62.02", "62.09"]
}}
"""
    try:
        text = await llm_complete(
            [{"role": "user", "content": prompt}],
            temperature=0.1, max_tokens=500, rounds=2,
        )
        import json
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
    except Exception:
        return {
            "nace_code": "",
            "nace_description": "Sektör açıklamanızı biraz daha detaylandırıp tekrar deneyin.",
            "is_kosgeb_eligible": False,
            "confidence": "low",
            "alternative_codes": [],
        }

    # ── Resmi NACE listesiyle doğrula (halüsinasyon kodları ele) ──
    from app.utils.nace_list import normalize_nace

    main = normalize_nace(str(result.get("nace_code", "")))
    alts_raw = result.get("alternative_codes", []) or []
    valid_alts = []
    for c in alts_raw:
        code_str = c.get("code") if isinstance(c, dict) else c
        n = normalize_nace(str(code_str or ""))
        if n:
            valid_alts.append(n)

    # Ana kod geçersizse, ilk geçerli alternatife düş; o da yoksa düşük güven
    if not main:
        if valid_alts:
            main = valid_alts.pop(0)
            result["confidence"] = "low"
        else:
            return {
                "nace_code": "",
                "nace_description": "Önerilen kod doğrulanamadı. Lütfen sektörünüzü daha açık tarif edin.",
                "is_kosgeb_eligible": False,
                "confidence": "low",
                "alternative_codes": [],
            }

    result["nace_code"] = main
    result["alternative_codes"] = valid_alts
    return result
