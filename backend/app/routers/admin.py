"""
Admin Panel Router
Sadece admin kullanıcılar erişebilir (is_admin=True)
GET  /api/admin/stats         — genel istatistikler
GET  /api/admin/users         — kullanıcı listesi
GET  /api/admin/payments      — ödeme listesi
PUT  /api/admin/programs/{id} — program güncelleme
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, date

from app.database import AsyncSessionLocal
from app.models import (
    User, Application, Payment, KosgebProgram,
    ProgramUpdateProposal, ProgramFetchLog, SiteContent, PricingPlan,
)
from app.schemas import ProgramResponse
from pydantic import BaseModel
from app.utils.deps import get_current_user

router = APIRouter(prefix="/api/admin", tags=["admin"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def require_admin(current_user: User = Depends(get_current_user)):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin erişimi gereklidir.")
    return current_user


@router.get("/stats")
async def get_stats(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    # Kullanıcı sayısı
    user_count = (await db.execute(select(func.count(User.id)))).scalar_one()
    # Başvuru sayısı
    app_count = (await db.execute(select(func.count(Application.id)))).scalar_one()
    # Ödeme sayısı ve toplam gelir
    paid_count = (await db.execute(
        select(func.count(Payment.id)).where(Payment.status == "paid")
    )).scalar_one()
    total_revenue = (await db.execute(
        select(func.coalesce(func.sum(Payment.amount), 0)).where(Payment.status == "paid")
    )).scalar_one()

    return {
        "user_count": user_count,
        "application_count": app_count,
        "paid_count": paid_count,
        "total_revenue_try": float(total_revenue),
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/users")
async def list_users(
    skip: int = 0,
    limit: int = 50,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return [
        {
            "id": str(u.id),
            "email": u.email,
            "name": u.name,
            "plan": u.plan,
            "credits": u.credits,
            "is_admin": getattr(u, "is_admin", False),
            "created_at": u.created_at.isoformat(),
        }
        for u in users
    ]


@router.get("/payments")
async def list_payments(
    skip: int = 0,
    limit: int = 50,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Payment).order_by(Payment.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()


class ProgramUpdateRequest(BaseModel):
    program_name: str | None = None
    max_support_amount: int | None = None
    application_period_start: str | None = None
    application_period_end: str | None = None
    is_active: bool | None = None
    required_documents: list[str] | None = None
    key_criteria: list[str] | None = None


@router.put("/programs/{program_id}")
async def update_program(
    program_id: str,
    req: ProgramUpdateRequest,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Admin: KOSGEB program bilgilerini güncelle."""
    result = await db.execute(select(KosgebProgram).where(KosgebProgram.id == uuid.UUID(program_id)))
    prog = result.scalar_one_or_none()
    if not prog:
        raise HTTPException(status_code=404, detail="Program bulunamadı.")

    if req.program_name is not None:
        prog.program_name = req.program_name
    if req.max_support_amount is not None:
        prog.max_support_amount = req.max_support_amount
    if req.application_period_start is not None:
        prog.application_period_start = date.fromisoformat(req.application_period_start)
    if req.application_period_end is not None:
        prog.application_period_end = date.fromisoformat(req.application_period_end)
    if req.is_active is not None:
        prog.is_active = req.is_active
    if req.required_documents is not None:
        prog.required_documents = req.required_documents
    if req.key_criteria is not None:
        prog.key_criteria = req.key_criteria

    prog.last_updated = datetime.utcnow()
    await db.commit()
    return {"message": "Program güncellendi.", "program_id": str(prog.id)}


# ─── PROGRAM OTO-GÜNCELLEME ÖNERİLERİ ────────────────────────────────────────

_DATE_FIELDS = ("application_period_start", "application_period_end")


def _proposed_to_kwargs(data: dict) -> dict:
    """proposed_data (JSON) → KosgebProgram alanları (ISO tarih → date)."""
    kwargs = dict(data or {})
    for f in _DATE_FIELDS:
        if kwargs.get(f):
            try:
                kwargs[f] = date.fromisoformat(str(kwargs[f]))
            except Exception:
                kwargs[f] = None
    return kwargs


@router.get("/programs/proposals")
async def list_proposals(
    status_filter: str = "pending",
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Onay bekleyen (veya verilen statüdeki) program değişiklik önerileri."""
    q = select(ProgramUpdateProposal).order_by(ProgramUpdateProposal.created_at.desc())
    if status_filter and status_filter != "all":
        q = q.where(ProgramUpdateProposal.status == status_filter)
    result = await db.execute(q)
    proposals = result.scalars().all()
    return [
        {
            "id": str(p.id),
            "program_code": p.program_code,
            "change_type": p.change_type,
            "proposed_data": p.proposed_data,
            "current_data": p.current_data,
            "diff_summary": p.diff_summary,
            "source_url": p.source_url,
            "confidence": p.confidence,
            "status": p.status,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in proposals
    ]


@router.post("/programs/proposals/{proposal_id}/approve")
async def approve_proposal(
    proposal_id: str,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Öneriyi onayla ve canlı kosgeb_programs tablosuna uygula."""
    result = await db.execute(
        select(ProgramUpdateProposal).where(ProgramUpdateProposal.id == uuid.UUID(proposal_id))
    )
    prop = result.scalar_one_or_none()
    if not prop or prop.status != "pending":
        raise HTTPException(status_code=404, detail="Bekleyen öneri bulunamadı.")

    if prop.change_type == "create":
        db.add(KosgebProgram(**_proposed_to_kwargs(prop.proposed_data)))
    elif prop.change_type == "update" and prop.program_id:
        prog_res = await db.execute(select(KosgebProgram).where(KosgebProgram.id == prop.program_id))
        prog = prog_res.scalar_one_or_none()
        if not prog:
            raise HTTPException(status_code=404, detail="Hedef program bulunamadı.")
        for field, value in _proposed_to_kwargs(prop.proposed_data).items():
            if value is not None and hasattr(prog, field):
                setattr(prog, field, value)
        prog.last_updated = datetime.utcnow()
    elif prop.change_type == "deactivate" and prop.program_id:
        prog_res = await db.execute(select(KosgebProgram).where(KosgebProgram.id == prop.program_id))
        prog = prog_res.scalar_one_or_none()
        if prog:
            prog.is_active = False

    prop.status = "approved"
    prop.reviewed_by = admin.id
    prop.reviewed_at = datetime.utcnow()
    await db.commit()
    return {"message": "Öneri onaylandı ve uygulandı.", "id": str(prop.id)}


class ProposalReject(BaseModel):
    note: str | None = None


@router.post("/programs/proposals/{proposal_id}/reject")
async def reject_proposal(
    proposal_id: str,
    req: ProposalReject,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ProgramUpdateProposal).where(ProgramUpdateProposal.id == uuid.UUID(proposal_id))
    )
    prop = result.scalar_one_or_none()
    if not prop or prop.status != "pending":
        raise HTTPException(status_code=404, detail="Bekleyen öneri bulunamadı.")
    prop.status = "rejected"
    prop.reviewed_by = admin.id
    prop.reviewed_at = datetime.utcnow()
    prop.review_note = req.note
    await db.commit()
    return {"message": "Öneri reddedildi.", "id": str(prop.id)}


@router.post("/programs/refresh")
async def refresh_programs(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """KOSGEB sitesinden hemen çek ve öneriler üret (canlıya dokunmaz)."""
    from app.services.program_scraper import run_scrape
    result = await run_scrape(db, triggered_by=f"admin:{admin.id}")
    return result


# ─── SİTE İÇERİĞİ (hero / istatistikler) ─────────────────────────────────────

@router.get("/content")
async def list_content(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(SiteContent).order_by(SiteContent.group, SiteContent.sort_order))
    return [
        {"key": c.key, "label": c.label, "value": c.value, "group": c.group, "sort_order": c.sort_order}
        for c in result.scalars().all()
    ]


class ContentUpdate(BaseModel):
    value: str | None = None
    label: str | None = None


@router.put("/content/{key}")
async def update_content(
    key: str,
    req: ContentUpdate,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(SiteContent).where(SiteContent.key == key))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="İçerik anahtarı bulunamadı.")
    if req.value is not None:
        item.value = req.value
    if req.label is not None:
        item.label = req.label
    await db.commit()
    return {"message": "İçerik güncellendi.", "key": key}


# ─── FİYATLANDIRMA (dinamik fiyat + kampanya) ────────────────────────────────

@router.get("/pricing")
async def list_pricing(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(PricingPlan).order_by(PricingPlan.sort_order))
    return [
        {
            "code": p.code, "name": p.name, "description": p.description,
            "price_try": round((p.price or 0) / 100, 2),
            "campaign_price_try": round(p.campaign_price / 100, 2) if p.campaign_price is not None else None,
            "campaign_label": p.campaign_label,
            "campaign_start": p.campaign_start.isoformat() if p.campaign_start else None,
            "campaign_end": p.campaign_end.isoformat() if p.campaign_end else None,
            "features": p.features or [],
            "is_active": p.is_active,
        }
        for p in result.scalars().all()
    ]


class PricingUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price_try: float | None = None              # TL — kuruşa çevrilir
    campaign_price_try: float | None = None     # TL; null gönderilirse kampanya kaldırılır
    clear_campaign: bool = False
    campaign_label: str | None = None
    campaign_start: str | None = None           # YYYY-MM-DD
    campaign_end: str | None = None
    features: list[str] | None = None
    is_active: bool | None = None


@router.put("/pricing/{code}")
async def update_pricing(
    code: str,
    req: PricingUpdate,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(PricingPlan).where(PricingPlan.code == code))
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan bulunamadı.")

    if req.name is not None:
        plan.name = req.name
    if req.description is not None:
        plan.description = req.description
    if req.price_try is not None:
        plan.price = int(round(req.price_try * 100))
    if req.features is not None:
        plan.features = req.features
    if req.is_active is not None:
        plan.is_active = req.is_active

    if req.clear_campaign:
        plan.campaign_price = None
        plan.campaign_label = None
        plan.campaign_start = None
        plan.campaign_end = None
    else:
        if req.campaign_price_try is not None:
            plan.campaign_price = int(round(req.campaign_price_try * 100))
        if req.campaign_label is not None:
            plan.campaign_label = req.campaign_label
        if req.campaign_start is not None:
            plan.campaign_start = date.fromisoformat(req.campaign_start) if req.campaign_start else None
        if req.campaign_end is not None:
            plan.campaign_end = date.fromisoformat(req.campaign_end) if req.campaign_end else None

    plan.updated_at = datetime.utcnow()
    await db.commit()
    return {"message": "Fiyat planı güncellendi.", "code": code}
