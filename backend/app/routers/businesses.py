import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Business, User
from app.schemas import BusinessCreate, BusinessUpdate, BusinessResponse
from app.utils.deps import get_current_user
from app.utils.security import encrypt_field

router = APIRouter(prefix="/api/businesses", tags=["businesses"])


@router.post("", response_model=BusinessResponse, status_code=status.HTTP_201_CREATED)
async def create_business(
    data: BusinessCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    business = Business(
        user_id=current_user.id,
        business_name=data.business_name,
        nace_code=data.nace_code,
        nace_description=data.nace_description,
        founding_date=data.founding_date,
        employee_count=data.employee_count,
        annual_revenue=data.annual_revenue,
        city=data.city,
        is_woman_entrepreneur=data.is_woman_entrepreneur,
        is_young_entrepreneur=data.is_young_entrepreneur,
        is_disabled=data.is_disabled,
        is_veteran=data.is_veteran,
        sector_description=data.sector_description,
        kosgeb_registered=data.kosgeb_registered,
        has_recent_partnership=data.has_recent_partnership,
        # Vergi numarası şifreli saklanır (KVKK)
        tax_number_encrypted=encrypt_field(data.tax_number) if data.tax_number else None,
    )
    db.add(business)
    await db.commit()
    await db.refresh(business)
    return business


@router.get("", response_model=list[BusinessResponse])
async def list_businesses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Business).where(Business.user_id == current_user.id))
    return result.scalars().all()


@router.get("/{business_id}", response_model=BusinessResponse)
async def get_business(
    business_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Business).where(Business.id == business_id, Business.user_id == current_user.id)
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="İşletme bulunamadı.")
    return business


@router.put("/{business_id}", response_model=BusinessResponse)
async def update_business(
    business_id: uuid.UUID,
    data: BusinessUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Business).where(Business.id == business_id, Business.user_id == current_user.id)
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="İşletme bulunamadı.")

    update_data = data.model_dump(exclude_unset=True, exclude={"tax_number"})
    for field, value in update_data.items():
        setattr(business, field, value)

    if data.tax_number is not None:
        business.tax_number_encrypted = encrypt_field(data.tax_number)

    await db.commit()
    await db.refresh(business)
    return business


@router.delete("/{business_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_business(
    business_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Business).where(Business.id == business_id, Business.user_id == current_user.id)
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="İşletme bulunamadı.")
    await db.delete(business)
    await db.commit()
