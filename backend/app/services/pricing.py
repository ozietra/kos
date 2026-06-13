"""
Fiyatlandırma servisi: geçerli fiyatı (kampanya aktifse indirimli) hesaplar.
Ödeme tutarı DAİMA buradan alınır — frontend'den gelen tutara güvenilmez.
"""
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import PricingPlan


def is_campaign_active(plan: PricingPlan, today: date | None = None) -> bool:
    today = today or date.today()
    if plan.campaign_price is None:
        return False
    if plan.campaign_start and today < plan.campaign_start:
        return False
    if plan.campaign_end and today > plan.campaign_end:
        return False
    return True


def effective_price_kurus(plan: PricingPlan, today: date | None = None) -> int:
    """Ödenecek gerçek tutar (kuruş)."""
    if is_campaign_active(plan, today):
        return plan.campaign_price
    return plan.price


def _tl(kurus: int | None) -> float:
    return round((kurus or 0) / 100, 2)


def plan_to_public_dict(plan: PricingPlan, today: date | None = None) -> dict:
    active = is_campaign_active(plan, today)
    eff = effective_price_kurus(plan, today)
    return {
        "code": plan.code,
        "name": plan.name,
        "description": plan.description,
        "features": plan.features or [],
        "currency": plan.currency,
        "price": _tl(plan.price),                # normal fiyat (TL)
        "effective_price": _tl(eff),             # ödenecek fiyat (TL)
        "is_campaign": active,
        "campaign_label": plan.campaign_label if active else None,
        "campaign_end": plan.campaign_end.isoformat() if (active and plan.campaign_end) else None,
        "is_active": plan.is_active,
    }


async def get_active_plans(db: AsyncSession) -> list[dict]:
    res = await db.execute(
        select(PricingPlan).where(PricingPlan.is_active == True).order_by(PricingPlan.sort_order)
    )
    return [plan_to_public_dict(p) for p in res.scalars().all()]


async def get_plan_by_code(db: AsyncSession, code: str) -> PricingPlan | None:
    res = await db.execute(select(PricingPlan).where(PricingPlan.code == code))
    return res.scalar_one_or_none()
