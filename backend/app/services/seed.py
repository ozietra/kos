"""
KOSGEB Program seed verisi — Mart 2026 itibarıyla güncel
"""
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import KosgebProgram


PROGRAMS_SEED = [
    {
        "program_name": "Girişimci Destek Programı — İş Geliştirme Desteği",
        "program_code": "IGD-2026",
        "max_support_amount": 1_500_000,
        "support_type": "hibe",
        "eligible_nace_prefixes": [
            "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
            "30", "31", "32", "33",   # C: İmalat
            "61",                       # Telekomünikasyon
            "62",                       # Bilgisayar programlama
            "63",                       # Bilişim altyapısı
            "72",                       # Ar-Ge
        ],
        "min_business_age_months": 0,
        "max_business_age_months": 36,  # 0-3 yaş
        "application_period_start": date(2026, 4, 1),
        "application_period_end": date(2026, 4, 30),
        "required_documents": [
            "İşyeri açma ve çalışma ruhsatı",
            "Vergi levhası",
            "Ticaret sicil gazetesi",
            "İmza sirküleri",
            "KOSGEB Veri Tabanı kayıt belgesi",
            "Proje başvuru formu",
            "İş planı",
            "Bütçe tablosu",
            "Proforma faturalar (planlanan alımlar için)",
        ],
        "key_criteria": [
            "İşletme 0-3 yıllık olmalı",
            "KOSGEB veri tabanında kayıtlı olmalı",
            "Vergi ve SGK borcu bulunmamalı",
            "Son 3 yılda başka işletmede %25+ ortaklık bulunmamalı",
            "NACE kodu uygun sektörlerden biri olmalı",
        ],
        "is_active": True,
    },
    {
        "program_name": "KOBİGEL — KOBİ Gelişim Destek Programı (2026 1. Çağrı)",
        "program_code": "KOBIGEL-2026-1",
        "max_support_amount": 5_000_000,
        "support_type": "hibe",
        "eligible_nace_prefixes": [
            "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
            "30", "31", "32", "33",
            "61", "62", "63", "72",
        ],
        "min_business_age_months": 12,
        "max_business_age_months": None,  # Üst sınır yok
        "application_period_start": date(2026, 3, 15),
        "application_period_end": date(2026, 4, 30),
        "required_documents": [
            "İşyeri açma ve çalışma ruhsatı",
            "Vergi levhası",
            "Ticaret sicil gazetesi",
            "Son 2 yıl mali tablolar",
            "Bağımsız denetim raporu (gerekirse)",
            "Proje başvuru formu",
            "Detaylı iş planı ve fizibilite",
            "Ar-Ge personel listesi (varsa)",
        ],
        "key_criteria": [
            "KOBİ ölçeğinde işletme olmalı (250 kişinin altında)",
            "2026 öncelikli alanlar: Dijital Dönüşüm, Yeşil Sanayi",
            "Yüksek teknoloji veya orta-yüksek teknoloji sektör",
            "Vergi borcu ve SGK borcu bulunmamalı",
        ],
        "is_active": True,
    },
    {
        "program_name": "Kapasite Geliştirme Desteği — Kredi Faiz Desteği",
        "program_code": "KGD-2026",
        "max_support_amount": 20_000_000,
        "support_type": "kredi_faiz",
        "eligible_nace_prefixes": [
            "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
            "30", "31", "32", "33",
            "61", "62", "63", "72",
        ],
        "min_business_age_months": 24,
        "max_business_age_months": None,
        "application_period_start": date(2026, 1, 1),
        "application_period_end": date(2026, 12, 31),
        "required_documents": [
            "İşyeri açma ve çalışma ruhsatı",
            "Banka kredi sözleşmesi",
            "Proforma faturalar",
            "Vergi levhası",
            "Mali tablolar",
        ],
        "key_criteria": [
            "En az 2 yıllık işletme",
            "Üretim kapasitesi artırımı veya teknoloji yenileme amaçlı",
            "İlk 24 ay ödemesiz, toplam 36 ay vade",
        ],
        "is_active": True,
    },
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
