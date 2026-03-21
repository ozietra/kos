import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Business, EligibilityCheck, User
from app.schemas import EligibilityResult, EligibleProgram, IneligibleProgram, EligibilityWarning
from app.services.eligibility import check_eligibility
from app.utils.deps import get_current_user

router = APIRouter(prefix="/api/eligibility", tags=["eligibility"])


@router.post("/check", response_model=EligibilityResult)
async def run_eligibility_check(
    business_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # İşletme sahipliği kontrolü
    result = await db.execute(
        select(Business).where(Business.id == business_id, Business.user_id == current_user.id)
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="İşletme bulunamadı.")

    check_result = await check_eligibility(business, db)

    return EligibilityResult(
        business_id=business.id,
        eligible=[
            EligibleProgram(
                program_id=e.program_id,
                program_name=e.program_name,
                max_amount=e.max_amount,
                support_type=e.support_type,
                key_requirements=e.key_requirements,
                next_step=e.next_step,
                application_deadline=e.application_deadline,
            )
            for e in check_result.eligible
        ],
        ineligible=[
            IneligibleProgram(
                program_name=i.program_name,
                reason=i.reason,
                could_be_eligible_if=i.could_be_eligible_if,
            )
            for i in check_result.ineligible
        ],
        warnings=[
            EligibilityWarning(type=w.type, message=w.message)
            for w in check_result.warnings
        ],
    )


@router.get("/{business_id}", response_model=EligibilityResult | None)
async def get_last_eligibility(
    business_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # İşletme sahipliği kontrolü
    biz_result = await db.execute(
        select(Business).where(Business.id == business_id, Business.user_id == current_user.id)
    )
    business = biz_result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="İşletme bulunamadı.")

    result = await db.execute(
        select(EligibilityCheck)
        .where(EligibilityCheck.business_id == business_id)
        .order_by(EligibilityCheck.created_at.desc())
        .limit(1)
    )
    check = result.scalar_one_or_none()
    if not check:
        return None

    # Eski veritabanı kayıtlarındaki eksik alanları tolere et
    eligible_list = []
    for p in (check.eligible_programs or []):
        p.setdefault("key_requirements", [])
        p.setdefault("next_step", "Başvuru adımlarını takip edin.")
        p.setdefault("application_deadline", None)
        eligible_list.append(EligibleProgram(**p))

    ineligible_list = []
    for p in (check.ineligible_programs or []):
        p.setdefault("could_be_eligible_if", None)
        ineligible_list.append(IneligibleProgram(**p))

    return EligibilityResult(
        business_id=business_id,
        eligible=eligible_list,
        ineligible=ineligible_list,
        warnings=[EligibilityWarning(**w) for w in (check.warnings or [])],
    )
