"""
AI Başvuru Metni Üretici — Groq Llama-3 Altyapısı (Faz 6)
Kademeli üretim (Chunking) ve %90 Başarı (Self-Correction) filtreli
"""
import os
import asyncio
from typing import AsyncGenerator
from groq import AsyncGroq
from app.config import settings

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

# ─── SİSTEM PROMPTLARI (Mart 2026 KOSGEB Standartları) ─────────────────────────

SYSTEM_PROMPT = """Sen üst düzey bir KOSGEB Proje Değerlendirme Uzmanı ve Danışmanısın.
Mart 2026 itibarıyla KOSGEB'in beklentileri:
- Gerçekçi, ölçülebilir ve somut hedefler (Afaki rakamlar reddediliyor).
- Dijital dönüşüm, yeşil enerji ve yerli üretim projelerine tam destek.
- Şişirilmiş bütçeler onay almıyor, her talep mantıklı bir "Neden?" ile açıklanmalı.

KURALLAR:
- "Tabii ki", "Kesinlikle", "Anlaşıldı", "İşte metniniz" gibi yapay zeka kalıplarını ASLA KULLANMA. Doğrudan metni ver.
- Mutevazı ama vizyoner bir dil kullan. Bürokratik, soğuk ama akıcı bir Türkçe tercih et.
- Onay şansını %90'ın üzerine çıkaracak "Gerekçe-Sonuç" mantığıyla yaz.
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
            return response.choices[0].message.content.strip()
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

Değerlendirme Kriterleri (Mart 2026 Standartları):
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
    return template.format(**fill)


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
        return json.loads(text)
    except Exception as e:
        return {
            "nace_code": "00.00",
            "nace_description": f"Sorgu hatası: {str(e)[:50]}",
            "is_kosgeb_eligible": False,
            "confidence": "low",
            "alternative_codes": []
        }
