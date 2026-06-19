"""
KOSGEB Program seed verisi — Güncel KOSGEB programları (2024-2026)
"""
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import KosgebProgram, User, SiteContent, PricingPlan
from app.config import settings


PROGRAMS_SEED = [
    {
        "program_name": "Girişimci Destek Programı — İş Geliştirme Desteği",
        "program_code": "IGD-2026",
        "max_support_amount": 2_000_000,
        "support_type": "geri_odemeli",
        "eligible_nace_prefixes": [
            "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
            "30", "31", "32", "33",   # İmalat
            "61", "62", "63", "72",   # Bilişim / Ar-Ge
        ],
        "min_business_age_months": 0,
        "max_business_age_months": 36,  # 0-3 yaş
        "application_period_start": date(2026, 1, 1),
        "application_period_end": date(2026, 12, 31),
        "required_documents": [
            "İşyeri açma ve çalışma ruhsatı",
            "Vergi levhası",
            "Ticaret sicil gazetesi",
            "KOSGEB Veri Tabanı kayıt belgesi",
            "İş planı",
            "Bütçe tablosu",
        ],
        "key_criteria": [
            "İşletme 0-3 yıllık olmalı",
            "İmalat veya bilişim/Yazılım sektöründe olmalı",
            "Son 3 yılda başka işletmede %25+ ortaklık bulunmamalı",
        ],
        "is_active": True,
    },
    {
        "program_name": "Girişimci Destek Programı — İş Kurma Desteği",
        "program_code": "IKD-2026",
        "max_support_amount": 20_000,
        "support_type": "hibe",
        "eligible_nace_prefixes": None, # Tüm sektörler başvuru yapabilir
        "min_business_age_months": 0,
        "max_business_age_months": 12,  # 0-1 yaş
        "application_period_start": date(2026, 1, 1),
        "application_period_end": date(2026, 12, 31),
        "required_documents": [
            "Vergi levhası",
            "Ticaret sicil gazetesi",
        ],
        "key_criteria": [
            "Kuruluşundan 1 yıl geçmemiş işletmeler",
            "Şahıs işletmelerine 10.000 TL, sermaye şirketlerine 20.000 TL",
            "Genç, Kadın ve Engelli girişimcilere 10.000 TL ek destek",
        ],
        "is_active": True,
    },
    {
        "program_name": "KOBİ Dijital Dönüşüm Destek Programı",
        "program_code": "KOBIDIJ-2026",
        "max_support_amount": 20_000_000,
        "support_type": "karma",
        "eligible_nace_prefixes": None,
        "min_business_age_months": 24, # En az 2 yıllık olmalı
        "max_business_age_months": None,
        "application_period_start": date(2026, 1, 1),
        "application_period_end": date(2026, 12, 31),
        "required_documents": [
            "TÜBİTAK DDX (Dijital Dönüşüm Değerlendirme) Raporu",
            "Kapasite Raporu",
            "Bağımsız denetim raporu",
            "Proforma faturalar",
        ],
        "key_criteria": [
            "KOBİ Bilgi Sistemi kayıtlı ve beyannamesi onaylı olmalı",
            "Dijital Dönüşüm Yol Haritası veya olgunluk değerlendirme raporuna sahip olmalı",
            "Üretim süreçlerinde dijitalleşme vizyonu",
            "Kredi Ust Limiti: 20.000.000 TL, Kredi Alt Limiti: 1.000.000 TL",
            "Destek Puanı: 20 (Geri Ödemesiz)",
            "Program Süresi: 24 Ay, Azami Kredi Vadesi: 36 Ay"
        ],
        "is_active": True,
    },
    {
        "program_name": "Kapasite Geliştirme Destek Programı",
        "program_code": "KGD-2026",
        "max_support_amount": 20_000_000,
        "support_type": "kredi_faiz",
        "eligible_nace_prefixes": None,
        "min_business_age_months": 12,
        "max_business_age_months": None,
        "application_period_start": date(2026, 2, 1),
        "application_period_end": date(2026, 12, 31),
        "required_documents": [
            "İşyeri açma ruhsatı",
            "Banka kredi sözleşmesi taslağı",
            "Makine ve teçhizat proformaları",
            "SGK Borcu Yoktur yazısı",
        ],
        "key_criteria": [
            "Kapasite artırımı / üretim parkuru genişlemesi amaçlanmalı",
            "İlk 24 ay ödemesiz seçenekler",
            "Kadın veya genç işletme sahiplerine faiz indirimleri",
        ],
        "is_active": True,
    },
    {
        "program_name": "Küresel Rekabetçilik Destek Programı",
        "program_code": "KURESEL-2026",
        "max_support_amount": 10_000_000,
        "support_type": "karma",
        "eligible_nace_prefixes": None, # Odak ihracatçı ve imalatçılar
        "min_business_age_months": 12,
        "max_business_age_months": None,
        "application_period_start": date(2026, 1, 1),
        "application_period_end": date(2026, 12, 31),
        "required_documents": [
            "Yurtdışı Pazar Araştırması",
            "İhracat/Gümrük Beyannameleri (varsa)",
            "Yurtdışı fuar kayıt belgeleri",
        ],
        "key_criteria": [
            "Uluslararası pazarlara açılma potansiyeli",
            "Yurtdışı fuar, pazar araştırması ve sertifikasyon giderlerinin desteklenmesi",
        ],
        "is_active": True,
    },
    {
        "program_name": "İstihdamı Koruma Destek Programı",
        "program_code": "ISTKOR-2026",
        "max_support_amount": 1_500_000,
        "support_type": "hibe",
        "eligible_nace_prefixes": None,
        "min_business_age_months": 6,
        "max_business_age_months": None,
        "application_period_start": date(2026, 1, 1),
        "application_period_end": date(2026, 12, 31),
        "required_documents": [
            "Aylık prim ve hizmet belgeleri",
            "Hasar Tespit Raporu (Deprem vs. Özel Durumlar İçin)",
        ],
        "key_criteria": [
            "Mikro ve Küçük İşletmeler",
            "Doğrudan hasar görmüş veya istihdam taahhüdüne uyan işletmeler",
        ],
        "is_active": True,
    },
    {
        "program_name": "TEKMER'ler (Teknoloji Merkezi) Destek Programı",
        "program_code": "TEKMER-2026",
        "max_support_amount": 6_000_000,
        "support_type": "karma",
        "eligible_nace_prefixes": ["72", "74", "85"], # Eğitim, Arge, Danışmanlık
        "min_business_age_months": 0,
        "max_business_age_months": None,
        "application_period_start": date(2026, 1, 1),
        "application_period_end": date(2026, 12, 31),
        "required_documents": [
            "Üniversite / Özel Sektör protokolleri",
            "Mimari ve teknik fizibilite",
        ],
        "key_criteria": [
            "İşletici kuruluş olmalı (Üniversite - Özel Sektör ortaklığı)",
            "Kuluçka merkezi hizmeti sunmalı",
        ],
        "is_active": True,
    },
    {
        "program_name": "SEGEM (Sektörel Gelişim Merkezi) Destek Programı",
        "program_code": "SEGEM-2026",
        "max_support_amount": 10_000_000,
        "support_type": "geri_odemeli",
        "eligible_nace_prefixes": None,
        "min_business_age_months": 24,
        "max_business_age_months": None,
        "application_period_start": date(2026, 1, 1),
        "application_period_end": date(2026, 12, 31),
        "required_documents": [
            "Sektörel gelişim kapasite raporu",
            "İşletici kuruluş sözleşmesi",
        ],
        "key_criteria": [
            "Belirli bir sektörün dönüşümüne hizmet eden mükemmeliyet merkezleri",
            "Eğitim, danışmanlık, model fabrika benzeri hizmetler vermeli",
        ],
        "is_active": True,
    }
]


async def seed_programs(db: AsyncSession) -> None:
    """Program seed verisi — sadece yoksa ekle"""
    for program_data in PROGRAMS_SEED:
        existing = await db.execute(
            select(KosgebProgram).where(KosgebProgram.program_code == program_data["program_code"])
        )
        if not existing.scalar_one_or_none():
            program = KosgebProgram(**program_data)
            db.add(program)

    await db.commit()
    print("✓ KOSGEB program seed verisi yüklendi.")


SITE_CONTENT_SEED = [
    {"key": "hero_badge_override", "label": "Hero rozeti (boşsa otomatik tarihten üretilir)", "value": "", "group": "hero", "sort_order": 0},
    {"key": "stat_total_grant", "label": "2025 yılında dağıtılan toplam hibe", "value": "2.45 Milyar ₺", "group": "stats", "sort_order": 1},
    {"key": "stat_project_count", "label": "Desteklenen proje sayısı (2025)", "value": "1.699", "group": "stats", "sort_order": 2},
    {"key": "stat_special_limit", "label": "Kadın/Genç/Engelli girişimcilere hibe limiti", "value": "1.650.000 ₺", "group": "stats", "sort_order": 3},
    {"key": "stat_periods", "label": "Yılda açılan başvuru dönemi", "value": "3", "group": "stats", "sort_order": 4},
    # SEO / Analitik entegrasyonları (admin panelinden doldurulur, siteye otomatik enjekte edilir)
    {"key": "google_analytics_id", "label": "Google Analytics Ölçüm Kimliği (G-XXXXXXX)", "value": "", "group": "seo", "sort_order": 10},
    {"key": "google_search_console", "label": "Google Search Console doğrulama kodu (meta içeriği)", "value": "", "group": "seo", "sort_order": 11},
]


async def seed_site_content(db: AsyncSession) -> None:
    """Site içeriği seed — sadece yoksa ekle."""
    for item in SITE_CONTENT_SEED:
        existing = await db.execute(select(SiteContent).where(SiteContent.key == item["key"]))
        if not existing.scalar_one_or_none():
            db.add(SiteContent(**item))
    await db.commit()


PRICING_SEED = [
    {
        "code": "starter", "name": "Starter", "description": "Tek seferlik, KDV dahil",
        "price": 49900, "currency": "TRY", "sort_order": 1,
        "features": ["Tam başvuru dosyası", "Profesyonel PDF çıktısı", "Belge kontrol listesi", "30 gün erişim"],
    },
    {
        "code": "pro", "name": "Pro", "description": "Çoklu başvuru + öncelikli destek",
        "price": 99900, "currency": "TRY", "sort_order": 2,
        "features": ["Sınırsız başvuru dosyası", "Profesyonel PDF çıktısı", "Belge kontrol listesi", "90 gün erişim", "Öncelikli destek"],
    },
]


async def seed_pricing_plans(db: AsyncSession) -> None:
    """Fiyat planı seed — sadece yoksa ekle."""
    for item in PRICING_SEED:
        existing = await db.execute(select(PricingPlan).where(PricingPlan.code == item["code"]))
        if not existing.scalar_one_or_none():
            db.add(PricingPlan(**item))
    await db.commit()


async def bootstrap_admin(db: AsyncSession) -> None:
    """
    ADMIN_EMAIL ayarlıysa, o e-postaya sahip MEVCUT kullanıcıyı admin yapar.
    Güvenli: yoksa hiçbir şey yapmaz, varsayılan admin oluşturmaz. İdempotent.
    """
    email = (settings.ADMIN_EMAIL or "").strip().lower()
    if not email:
        return
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user and not user.is_admin:
        user.is_admin = True
        await db.commit()
        print(f"✓ Admin yetkisi verildi: {email}")
