"""
AI Başvuru Metni Üretici — Bölüm 5'teki tüm prompt şablonları
Gemini 2.5 Flash ile SSE streaming destekli
"""
from app.services.gemini import generate_text


# ─── PROMPT ŞABLONLARI ────────────────────────────────────────────────────────

PROJECT_SUMMARY_PROMPT = """
Sen deneyimli bir KOSGEB başvuru danışmanısın.
Aşağıdaki bilgilere göre KOSGEB İş Geliştirme Desteği için proje özeti yaz.

KRİTİK KURALLAR:
- İlk cümle projeyi ve hedefini net söylesin
- 2026 KOSGEB öncelikleriyle örtüşen noktaları öne çıkar (dijitalleşme, yeşil sanayi)
- Ölçülebilir hedefler kullan ("büyük büyüme" değil, "12 ayda 500 müşteri")
- Türkiye ekonomisine katkıyı vurgula: istihdam sayısı, gelir, ihracat potansiyeli
- "İnovatif", "devrimci", "benzersiz" gibi boş kelimeler kullanma
- "Tabii ki", "Kesinlikle", "Bu bağlamda", "Önemle belirtmek gerekir" gibi yapay zeka kalıplarından kaçın
- Yalın, akıcı Türkçe — bürokratik ama anlaşılır
- "Tabii ki", "Kesinlikle", "Bu bağlamda", "Sonuç itibarıyla", "Mükemmel bir fırsat" YASAK

İŞLETME BİLGİLERİ:
İşletme adı: {business_name}
NACE kodu: {nace_code}
Şehir: {city}
İşletme yaşı: {business_age_months} aylık
Özel kategori: {special_category}

PROJE BİLGİLERİ:
Proje başlığı: {project_title}
Fikir ve amaç: {project_idea}
Çözülen problem: {problem_solved}

PAZAR BİLGİLERİ:
Hedef kitle: {target_market}
Rekabet farkı: {competitive_advantage}
Pazar büyüklüğü: {market_size}

FİNANSAL:
Talep edilen destek: {requested_amount} TL
Bütçe kalemleri: {budget_items}
İlk yıl gelir hedefi: {revenue_target_year1} TL
İstihdam hedefi: {employment_target} kişi

400-600 kelime, paragraf halinde, başlıksız yaz.
""".strip()


BUSINESS_PLAN_PROMPT = """
Sen deneyimli bir KOSGEB başvuru danışmanısın.
Aynı bilgileri kullanarak resmi KOSGEB iş planı formatında yaz.

KRİTİK KURALLAR:
- Jüri anlayacak şekilde somut ve ölçülebilir bil
- "Tabii ki", "Kesinlikle", "Bu bağlamda", "Sonuç itibarıyla" YASAK
- "Tabii ki", "Mükemmel fırsat", "Büyük potansiyel" gibi boş ifadeler YASAK

İŞLETME: {business_name} | {nace_code} | {city} | {business_age_months} aylık
PROJE: {project_title}
FİKİR: {project_idea}
HEDEF KİTLE: {target_market}
REKABETÇİ AVANTAJ: {competitive_advantage}
BÜTÇE: {requested_amount} TL → {budget_items}
İSTİHDAM: {employment_target} kişi | GELİR HEDEFİ: {revenue_target_year1} TL
SÜRE: {project_duration_months} ay
KİLOMETRE TAŞLARI: {milestones}

Aşağıdaki başlıkları içer, her bölüm 100-200 kelime:

## 1. Pazar Analizi
## 2. Değer Önerisi  
## 3. İş Modeli
## 4. Pazarlama ve Satış Stratejisi
## 5. Operasyonel Plan
## 6. Riskler ve Önlemler
(3 risk: her biri için risk adı, olasılık, azaltma stratejisi)
""".strip()


FINANCIAL_PROJECTION_PROMPT = """
Sen deneyimli bir KOSGEB başvuru danışmanısın.
Aşağıdaki finansal bilgilere dayanarak 3 yıllık finansal projeksiyonun
neden gerçekçi olduğunu açıklayan metin yaz.

Bütçe kalemleri: {budget_items}
Toplam talep: {requested_amount} TL
1. yıl gelir hedefi: {revenue_target_year1} TL
İstihdam: {employment_target} kişi
Sektör: {nace_code} - {nace_description}

KURALLAR:
- Gerçekçi-iyimser ton
- Tablo değil, metin formatında
- "Tabii ki", "Kesinlikle" gibi yapay zeka kalıpları YASAK
- Somut gerekçeler ver (pazar büyüklüğü, talep trendi, maliyet yapısı)
- 200-300 kelime
""".strip()


TIMELINE_PROMPT = """
Sen deneyimli bir KOSGEB başvuru danışmanısın.
Aşağıdaki bilgilere dayanarak KOSGEB başvurusu için proje takvimi yaz.

Proje süresi: {project_duration_months} ay
Kilometre taşları: {milestones}
Proje başlığı: {project_title}
Bütçe kalemleri: {budget_items}

Her ay veya dönem için ne yapılacağını listele.
Format: "Ay X-Y: [Faaliyet açıklaması]" şeklinde.
Toplam 100-200 kelime, net ve takip edilebilir.
""".strip()


# ─── Belge Kontrol Listesi ────────────────────────────────────────────────────

DOCUMENT_CHECKLIST = {
    "IGD": [  # İş Geliştirme Desteği
        {
            "id": "ruhsat",
            "name": "İşyeri Açma ve Çalışma Ruhsatı",
            "description": "Belediyeden alınır. İşletmenin faaliyet adresine ait olmalı.",
            "where_to_get": "İlçe Belediyesi Ruhsat Müdürlüğü",
            "required": True,
        },
        {
            "id": "vergi_levhasi",
            "name": "Vergi Levhası",
            "description": "Güncel, dijital baskı kabul edilir.",
            "where_to_get": "Gelir İdaresi Başkanlığı (gib.gov.tr) / İnteraktif Vergi Dairesi",
            "required": True,
        },
        {
            "id": "ticaret_sicil",
            "name": "Ticaret Sicil Gazetesi",
            "description": "Şirket kuruluş gazetesi ve varsa değişiklik gazeteleri.",
            "where_to_get": "Türkiye Ticaret Sicili Gazetesi (ticaretsicilgazetesi.gtb.gov.tr)",
            "required": True,
        },
        {
            "id": "imza_sirküleri",
            "name": "İmza Sirküleri",
            "description": "Noterden onaylı, son 2 yıl içinde alınmış.",
            "where_to_get": "Herhangi bir noter",
            "required": True,
        },
        {
            "id": "kosgeb_kayit",
            "name": "KOSGEB Veri Tabanı Kayıt Belgesi",
            "description": "KOSGEB portalından alınır. Aktif statüde olmalı.",
            "where_to_get": "KOSGEB E-Hizmet Portalı (eportal.kosgeb.gov.tr)",
            "required": True,
        },
        {
            "id": "is_plani",
            "name": "İş Planı",
            "description": "Bu platform tarafından hazırlanmaktadır.",
            "where_to_get": "kosgebhibe.com (hazır)",
            "required": True,
        },
        {
            "id": "proje_ozeti",
            "name": "Proje Özeti",
            "description": "Bu platform tarafından hazırlanmaktadır.",
            "where_to_get": "kosgebhibe.com (hazır)",
            "required": True,
        },
        {
            "id": "butce_tablosu",
            "name": "Bütçe Tablosu",
            "description": "Planlanan harcamaların detaylı listesi.",
            "where_to_get": "Bu platform (PDF içinde hazır)",
            "required": True,
        },
        {
            "id": "proforma",
            "name": "Proforma Faturalar",
            "description": "Satın alınacak her ürün/hizmet için en az 1 proforma.",
            "where_to_get": "Tedarikçi firmalardan alınır.",
            "required": True,
        },
        {
            "id": "nufus",
            "name": "Nüfus Cüzdanı Fotokopisi",
            "description": "Yetkili kişinin kimlik fotokopisi.",
            "where_to_get": "Nüfus cüzdanından çekilir.",
            "required": True,
        },
    ],
    "KOBIGEL": [
        {
            "id": "ruhsat", "name": "İşyeri Açma ve Çalışma Ruhsatı",
            "description": "Belediyeden alınır.",
            "where_to_get": "İlçe Belediyesi", "required": True,
        },
        {
            "id": "mali_tablolar", "name": "Son 2 Yıl Mali Tablolar",
            "description": "Bilanço ve gelir tablosu, YMM onaylı.",
            "where_to_get": "Mali müşavirinizden alınır.", "required": True,
        },
        {
            "id": "fizibilite", "name": "Fizibilite Raporu",
            "description": "Projenin teknik ve finansal fizibilite analizi.",
            "where_to_get": "Bu platform (Faz 2'de eklenecek)", "required": True,
        },
    ],
}


def generate_document_checklist(program_type: str) -> list[dict]:
    """Program tipine göre belge listesi üret"""
    key = "IGD"
    if "KOBIGEL" in program_type.upper() or "KOBİGEL" in program_type.upper():
        key = "KOBIGEL"
    return DOCUMENT_CHECKLIST.get(key, DOCUMENT_CHECKLIST["IGD"])


# ─── Ana üretim fonksiyonu ────────────────────────────────────────────────────

def build_prompt(template: str, inputs: dict) -> str:
    """Şablona verileri yerleştir, eksik değerleri 'belirtilmemiş' ile doldur"""
    from string import Formatter
    keys = [fname for _, fname, _, _ in Formatter().parse(template) if fname]
    fill = {k: inputs.get(k) or "belirtilmemiş" for k in keys}
    return template.format(**fill)


async def generate_project_summary(inputs: dict) -> str:
    return await generate_text(build_prompt(PROJECT_SUMMARY_PROMPT, inputs))


async def generate_business_plan(inputs: dict) -> str:
    return await generate_text(build_prompt(BUSINESS_PLAN_PROMPT, inputs))


async def generate_financial_projection(inputs: dict) -> str:
    return await generate_text(build_prompt(FINANCIAL_PROJECTION_PROMPT, inputs))


async def generate_timeline(inputs: dict) -> str:
    return await generate_text(build_prompt(TIMELINE_PROMPT, inputs))
