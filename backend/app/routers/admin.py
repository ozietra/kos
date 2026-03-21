"""
Admin Panel Router
Sadece admin kullanıcılar erişebilir (is_admin=True)
GET  /api/admin/stats         — genel istatistikler
GET  /api/admin/users         — kullanıcı listesi
GET  /api/admin/payments      — ödeme listesi
PUT  /api/admin/programs/{id} — program güncelleme
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from app.database import AsyncSessionLocal
from app.models import User, Application, Payment, KosgebProgram
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
    from datetime import date
    result = await db.execute(select(KosgebProgram).where(KosgebProgram.id == program_id))
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
