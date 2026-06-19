"""
AI Başvuru Metni Üretici — Groq Llama-3 Altyapısı (Faz 6)
Kademeli üretim (Chunking) ve %90 Başarı (Self-Correction) filtreli
"""
import os
import re
import asyncio
from datetime import date
from typing import AsyncGenerator
from groq import AsyncGroq
from app.config import settings

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


client = AsyncGroq(api_key=settings.GROQ_API_KEY)

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

YAZIM KURALLARI:
- Doğrudan dosya metnini yaz. "Tabii ki", "Kesinlikle", "Anlaşıldı", "İşte metniniz", "Umarım yardımcı olur" gibi sohbet/asistan kalıplarını ASLA kullanma.
- Profesyonel bir danışmanın ağzından, resmi ama akıcı, ikna edici ve özgüvenli bir Türkçe kullan.
- SADECE TÜRKÇE yaz. Hiçbir yabancı dil kelimesi veya farklı alfabe (Çince, Vietnamca vb.) kullanma.
- Hiçbir platform, marka, web sitesi veya yazılım adı geçirme. Metin, danışmanın işletme adına bizzat hazırladığı bir dosya gibi olmalı.
- "Gerekçe → Sonuç" mantığıyla, jüriyi ikna edecek ciddiyette yaz.
"""

# ─── YARDIMCI FONKSİYONLAR ──────────────────────────────────────────────────

async def call_groq(prompt: str, max_retries=2) -> str:
    """Temel Groq API çağrısı, 429 hatalarını gizler ve retry yapar."""
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                max_tokens=2500,
            )
            return _sanitize_tr(response.choices[0].message.content.strip())
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "rate limit" in err_str or "resource_exhausted" in err_str:
                if attempt < max_retries - 1:
                    await asyncio.sleep(3)
                    continue
                raise Exception("Analiz sunucularımızda anlık bir yoğunluk yaşanıyor. Lütfen işleminizi 1-2 dakika sonra tekrar deneyiniz.")
            raise Exception(f"Üretim Hatası: {str(e)}")


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
    eval_response = await call_groq(eval_prompt)
    if "<APPROVED>" in eval_response.upper():
        return text
    
    # Yeni metin üretildi, temizle ve döndür
    return eval_response.replace("<APPROVED>", "").strip()


def build_prompt(template: str, inputs: dict) -> str:
    from string import Formatter
    keys = [fname for _, fname, _, _ in Formatter().parse(template) if fname]
    fill = {k: inputs.get(k) or "belirtilmemiş" for k in keys}
    body = template.format(**fill)
    # Başvurulan programın gerçek bilgileri varsa, her bölümün başına ekle ki
    # metin o programın amacı/şartları/destek unsurlarına birebir uygun yazılsın.
    ctx = (inputs.get("program_context") or "").strip()
    if ctx:
        return (
            "BAŞVURULAN KOSGEB PROGRAMININ RESMİ BİLGİLERİ "
            "(metni bu programın amacı, başvuru şartları ve destek unsurlarına "
            "birebir uygun, bunlara atıfla yaz):\n"
            f"{ctx}\n\n---\n{body}"
        )
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
        response = await client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=500,
        )
        text = response.choices[0].message.content.strip()
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
