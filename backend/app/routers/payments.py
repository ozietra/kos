"""
Ödeme Router — iyzico + PayTR.

Tutar DAİMA veritabanındaki PricingPlan'dan (kampanya dahil) hesaplanır;
frontend'den gelen tutara güvenilmez. Başvuru sahipliği Business üzerinden
doğrulanır (Application'ın user_id'si yoktur).
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.config import settings
from app.database import AsyncSessionLocal
from app.models import Payment, Application, Business, User
from app.schemas import CheckoutRequest
from app.utils.deps import get_current_user
from app.services.payment import create_checkout_form, retrieve_checkout_result
from app.services.payment_paytr import create_payment_token, iframe_url, verify_callback
from app.services.pricing import get_plan_by_code, effective_price_kurus
from app.services.email import send_payment_confirmation

router = APIRouter(prefix="/api/payments", tags=["payments"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def _owned_application(db: AsyncSession, application_id, user_id) -> Application | None:
    result = await db.execute(
        select(Application).join(Business).where(
            Application.id == application_id,
            Business.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


@router.post("/checkout")
async def checkout(
    req: CheckoutRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    app = await _owned_application(db, req.application_id, current_user.id)
    if not app:
        raise HTTPException(status_code=404, detail="Başvuru bulunamadı.")
    if app.payment_status == "paid":
        raise HTTPException(status_code=400, detail="Bu başvuru için ödeme zaten alınmış.")

    plan = await get_plan_by_code(db, req.plan)
    if not plan or not plan.is_active:
        raise HTTPException(status_code=404, detail="Geçerli bir plan bulunamadı.")

    amount_kurus = effective_price_kurus(plan)  # kampanya dahil gerçek tutar
    client_ip = request.client.host if request.client else "0.0.0.0"

    # Bekleyen ödeme kaydı (önce oluştur → PayTR merchant_oid için id lazım)
    payment = Payment(
        user_id=current_user.id,
        application_id=req.application_id,
        plan=req.plan,
        product_type=req.plan,
        amount=amount_kurus,
        currency="TRY",
        provider=req.provider,
        status="pending",
    )
    db.add(payment)
    await db.flush()

    if req.provider == "paytr":
        merchant_oid = payment.id.hex  # alfanümerik, benzersiz
        data = await create_payment_token(
            merchant_oid=merchant_oid,
            user_email=current_user.email,
            amount_kurus=amount_kurus,
            user_name=current_user.name or current_user.email,
            plan_name=plan.name,
            user_ip=client_ip,
        )
        if data.get("status") != "success":
            await db.rollback()
            raise HTTPException(status_code=502, detail=f"PayTR hatası: {data.get('reason', 'bilinmeyen')}")
        payment.provider_reference = merchant_oid
        await db.commit()
        return {"provider": "paytr", "iframe_url": iframe_url(data["token"]), "token": data["token"]}

    # iyzico
    data = await create_checkout_form(
        user_id=str(current_user.id),
        user_email=current_user.email,
        user_name=current_user.name or current_user.email,
        plan=req.plan,
        plan_name=plan.name,
        price_tl=amount_kurus / 100,
        application_id=str(req.application_id),
        ip_address=client_ip,
    )
    if data.get("status") != "success":
        await db.rollback()
        raise HTTPException(status_code=502, detail=f"iyzico hatası: {data.get('errorMessage', 'bilinmeyen')}")
    payment.provider_reference = data.get("token")
    await db.commit()
    return {
        "provider": "iyzico",
        "checkoutFormContent": data.get("checkoutFormContent"),
        "paymentPageUrl": data.get("paymentPageUrl"),
        "token": data.get("token"),
    }


# ─── iyzico callback ─────────────────────────────────────────────────────────

@router.post("/callback")
async def iyzico_callback(request: Request, db: AsyncSession = Depends(get_db)):
    form = await request.form()
    token = form.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Token eksik.")

    data = await retrieve_checkout_result(token)
    if data.get("status") != "success" or data.get("paymentStatus") != "SUCCESS":
        await _mark_paid(db, token, success=False)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/odeme/basarisiz", status_code=303)

    await _mark_paid(db, token, success=True)
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/odeme/basarili", status_code=303)


# ─── PayTR callback (bildirim) ───────────────────────────────────────────────

@router.post("/paytr/callback")
async def paytr_callback(request: Request, db: AsyncSession = Depends(get_db)):
    """PayTR sunucudan-sunucuya bildirim. Mutlaka 'OK' dönülmeli."""
    form = dict(await request.form())
    if not verify_callback(form):
        return PlainTextResponse("PAYTR notification failed: bad hash", status_code=400)

    merchant_oid = form.get("merchant_oid", "")
    success = form.get("status") == "success"
    await _mark_paid(db, merchant_oid, success=success)
    return PlainTextResponse("OK")


# ─── Sorgu uçları ─────────────────────────────────────────────────────────────

@router.get("/result")
async def payment_result(token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Payment).where(Payment.provider_reference == token))
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Ödeme bulunamadı.")
    return {"status": payment.status, "plan": payment.plan, "provider": payment.provider}


@router.get("/my")
async def my_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Payment).where(Payment.user_id == current_user.id).order_by(Payment.created_at.desc())
    )
    return [
        {
            "id": str(p.id),
            "plan": p.plan,
            "provider": p.provider,
            "amount_try": round((p.amount or 0) / 100, 2),
            "currency": p.currency,
            "status": p.status,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "paid_at": p.paid_at.isoformat() if p.paid_at else None,
        }
        for p in result.scalars().all()
    ]


# ─── Yardımcı ─────────────────────────────────────────────────────────────────

async def _mark_paid(db: AsyncSession, provider_reference: str, success: bool):
    result = await db.execute(select(Payment).where(Payment.provider_reference == provider_reference))
    payment = result.scalar_one_or_none()
    if not payment:
        return
    if not success:
        payment.status = "failed"
        await db.commit()
        return
    if payment.status == "paid":
        return  # idempotent — tekrar bildirim gelirse

    payment.status = "paid"
    payment.paid_at = datetime.utcnow()

    # Başvuruyu paid işaretle
    if payment.application_id:
        app_res = await db.execute(select(Application).where(Application.id == payment.application_id))
        app = app_res.scalar_one_or_none()
        if app:
            app.payment_status = "paid"
    await db.commit()

    # Onay e-postası
    user_res = await db.execute(select(User).where(User.id == payment.user_id))
    user = user_res.scalar_one_or_none()
    if user:
        try:
            await send_payment_confirmation(
                email=user.email,
                name=user.name or user.email,
                plan=payment.plan or "starter",
                amount=(payment.amount or 0) / 100,
            )
        except Exception:
            pass
