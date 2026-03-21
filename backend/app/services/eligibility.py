"""
Uygunluk Motoru — Bölüm 4'teki iş kurallarının tam implementasyonu
"""
from datetime import date, datetime, timezone
from dataclasses import dataclass, field
from typing import Any
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Business, KosgebProgram, EligibilityCheck


@dataclass
class EligibleProgramResult:
    program_id: str
    program_name: str
    max_amount: int
    support_type: str
    key_requirements: list[str]
    next_step: str
    application_deadline: date | None


@dataclass
class IneligibleProgramResult:
    program_name: str
    reason: str
    could_be_eligible_if: str | None = None


@dataclass
class WarningResult:
    type: str  # critical, warning, info
    message: str


@dataclass
class EligibilityResultData:
    business_id: uuid.UUID
    eligible: list[EligibleProgramResult] = field(default_factory=list)
    ineligible: list[IneligibleProgramResult] = field(default_factory=list)
    warnings: list[WarningResult] = field(default_factory=list)


def _business_age_months(business: Business) -> int | None:
    if not business.founding_date:
        return None
    today = date.today()
    delta = (today.year - business.founding_date.year) * 12 + (
        today.month - business.founding_date.month
    )
    return delta


def _calculate_max_amount(business: Business, base_amount: int) -> int:
    """Kadın/Genç/Engelli/Gazi bonusu hesapla"""
    bonus = 0
    if business.is_woman_entrepreneur:
        bonus = 150_000
    elif business.is_young_entrepreneur:
        bonus = 150_000
    elif business.is_disabled:
        bonus = 150_000
    elif business.is_veteran:
        bonus = 150_000
    return base_amount + bonus


def _is_nace_eligible(nace_code: str | None, eligible_prefixes: list[str] | None) -> bool:
    if not nace_code or not eligible_prefixes:
        return False
    for prefix in eligible_prefixes:
        if nace_code.startswith(prefix):
            return True
    return False


def _check_single_program(business: Business, program: KosgebProgram, age_months: int | None) -> dict:
    """
    Tek bir program için uygunluk kontrolü.
    Dönüş: {"eligible": bool, "reason": str, "met_requirements": list}
    """
    met = []
    reason = None

    # 1. Yaş kontrolü
    if program.min_business_age_months is not None or program.max_business_age_months is not None:
        if age_months is None:
            reason = "İşletme kuruluş tarihi girilmemiş."
        elif program.min_business_age_months and age_months < program.min_business_age_months:
            min_y = program.min_business_age_months // 12
            reason = f"İşletmeniz en az {min_y} yıllık olmalı (şu an {age_months} aylık)."
        elif program.max_business_age_months and age_months > program.max_business_age_months:
            max_y = program.max_business_age_months // 12
            reason = f"Bu program en fazla {max_y} yıllık işletmelere açık (şu an {age_months} aylık)."
        else:
            met.append("İşletme yaşı uygun")

    if reason:
        return {"eligible": False, "reason": reason, "met_requirements": met}

    # 2. NACE kontrolü
    if program.eligible_nace_prefixes:
        if not _is_nace_eligible(business.nace_code, program.eligible_nace_prefixes):
            return {
                "eligible": False,
                "reason": f"Sektörünüz ({business.nace_code or 'belirtilmemiş'}) bu program için uygun değil.",
                "met_requirements": met,
            }
        met.append("Sektör kodu uygun")

    # 3. Başvuru dönemi aktif mi?
    today = date.today()
    if program.application_period_end and today > program.application_period_end:
        return {
            "eligible": False,
            "reason": f"Bu dönem başvuruları {program.application_period_end.strftime('%d/%m/%Y')} tarihinde kapandı.",
            "met_requirements": met,
        }
    if program.application_period_start and today < program.application_period_start:
        return {
            "eligible": False,
            "reason": f"Bu dönem başvuruları {program.application_period_start.strftime('%d/%m/%Y')} tarihinde açılacak.",
            "met_requirements": met,
        }

    if program.application_period_start:
        met.append("Başvuru dönemi açık")

    return {"eligible": True, "reason": None, "met_requirements": met}


async def check_eligibility(business: Business, db: AsyncSession) -> EligibilityResultData:
    result = EligibilityResultData(business_id=business.id)
    age_months = _business_age_months(business)

    # Tüm aktif programları çek
    programs_result = await db.execute(select(KosgebProgram).where(KosgebProgram.is_active == True))
    programs = programs_result.scalars().all()

    for program in programs:
        check = _check_single_program(business, program, age_months)

        if check["eligible"]:
            max_amount = _calculate_max_amount(business, program.max_support_amount or 0)
            result.eligible.append(
                EligibleProgramResult(
                    program_id=str(program.id),
                    program_name=program.program_name,
                    max_amount=max_amount,
                    support_type=program.support_type or "hibe",
                    key_requirements=check["met_requirements"],
                    next_step="Başvuru metninizi hazırlamak için 'Başvuru Başlat' butonunu kullanın.",
                    application_deadline=program.application_period_end,
                )
            )
        else:
            suggest = None
            if age_months is not None and program.max_business_age_months and age_months > program.max_business_age_months:
                suggest = "Başka programları inceleyin (KOBİGEL, Kapasite Geliştirme)."
            result.ineligible.append(
                IneligibleProgramResult(
                    program_name=program.program_name,
                    reason=check["reason"],
                    could_be_eligible_if=suggest,
                )
            )

    # ─── Uyarılar (Bölüm 9) ───────────────────────────────────────────────
    if not business.kosgeb_registered:
        result.warnings.append(
            WarningResult(
                type="critical",
                message=(
                    "KOSGEB Veri Tabanı kaydınızın güncel ve aktif olduğunu doğrulayın. "
                    "Kayıt olmadan başvuru değerlendirmeye alınmaz."
                ),
            )
        )

    if business.has_recent_partnership:
        result.warnings.append(
            WarningResult(
                type="warning",
                message=(
                    "Son 3 yılda başka bir şirkette yüzde eşiği üzeri ortaklığınız varsa "
                    "İş Geliştirme Desteğine uygun olmayabilirsiniz. "
                    "Lütfen mali müşavirinizle kontrol edin."
                ),
            )
        )

    if not business.nace_code:
        result.warnings.append(
            WarningResult(
                type="info",
                message="NACE kodu girilmemiş. Uygunluk analizi tamamlanabilmesi için NACE kodunuzu ekleyin.",
            )
        )

    # Sonucu veritabanına kaydet
    check_record = EligibilityCheck(
        business_id=business.id,
        eligible_programs=[
            {
                "program_id": e.program_id,
                "program_name": e.program_name,
                "max_amount": e.max_amount,
                "support_type": e.support_type,
            }
            for e in result.eligible
        ],
        ineligible_programs=[
            {"program_name": i.program_name, "reason": i.reason}
            for i in result.ineligible
        ],
        warnings=[
            {"type": w.type, "message": w.message}
            for w in result.warnings
        ],
    )
    db.add(check_record)
    await db.commit()

    return result
