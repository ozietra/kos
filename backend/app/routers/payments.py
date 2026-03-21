"""
iyzico Ödeme Router
POST /api/payments/checkout   → ödeme formu oluştur
POST /api/payments/callback   → iyzico callback (form post)
GET  /api/payments/result     → token ile sonuç sorgula
GET  /api/payments/my         → kullanıcı ödeme geçmişi
"""
import json
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.database import AsyncSessionLocal
from app.models import Payment, Application, User
from app.schemas import CheckoutRequest
from app.utils.deps import get_current_user
from app.services.payment import create_checkout_form, retrieve_checkout_result
from app.services.email import send_payment_confirmation

router = APIRouter(prefix="/api/payments", tags=["payments"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/checkout")
async def checkout(
    req: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    iyzico checkout form oluştur.
    Kullanıcı dönen URL'e yönlendirilir.
    """
    # Başvuru mevcut ve kullanıcıya ait mi?
    result = await db.execute(
        select(Application).where(
            Application.id == req.application_id,
            Application.user_id == current_user.id,
        )
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="Başvuru bulunamadı.")

    # Zaten ödeme yapılmış mı?
    if app.payment_status == "paid":
        raise HTTPException(status_code=400, detail="Bu başvuru için ödeme zaten alınmış.")

    data = await create_checkout_form(
        user_id=str(current_user.id),
        user_email=current_user.email,
        user_name=current_user.name or current_user.email,
        plan=req.plan,
        application_id=str(req.application_id),
    )

    if data.get("status") != "success":
        raise HTTPException(
            status_code=502,
            detail=f"iyzico hatası: {data.get('errorMessage', 'Bilinmeyen hata')}",
        )

    # Bekleyen ödeme kaydı oluştur
    payment = Payment(
        user_id=current_user.id,
        application_id=req.application_id,
        plan=req.plan,
        amount=499.0 if req.plan == "starter" else 999.0,
        currency="TRY",
        provider_reference=data.get("token"),
        status="pending",
    )
    db.add(payment)
    await db.commit()

    return {
        "checkoutFormContent": data.get("checkoutFormContent"),
        "paymentPageUrl": data.get("paymentPageUrl"),
        "token": data.get("token"),
    }


@router.post("/callback")
async def callback(request: Request, db: AsyncSession = Depends(get_db)):
    """
    iyzico form POST callback — HTTPS üretimde çalışır.
    token ile ödeme sonucunu doğrular.
    """
    form = await request.form()
    token = form.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Token eksik.")

    data = await retrieve_checkout_result(token)

    if data.get("status") != "success" or data.get("paymentStatus") != "SUCCESS":
        # Ödeme başarısız
        await _update_payment(db, token, "failed")
        # Kullanıcıyı hata sayfasına yönlendir
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/odeme/basarisiz", status_code=303)

    user, payment = await _update_payment(db, token, "paid")

    # Başvuruyu "paid" olarak işaretle
    if payment:
        result = await db.execute(
            select(Application).where(Application.id == payment.application_id)
        )
        app = result.scalar_one_or_none()
        if app:
            app.payment_status = "paid"
            await db.commit()

        # Onay e-postası gönder
        if user:
            await send_payment_confirmation(
                email=user.email,
                name=user.name or user.email,
                plan=payment.plan,
                amount=payment.amount,
            )

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/odeme/basarili", status_code=303)


@router.get("/result")
async def payment_result(
    token: str,
    db: AsyncSession = Depends(get_db),
):
    """Frontend'in token ile sonucu yoklaması için."""
    result = await db.execute(
        select(Payment).where(Payment.provider_reference == token)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Ödeme bulunamadı.")
    return {"status": payment.status, "plan": payment.plan}


@router.get("/my")
async def my_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Payment)
        .where(Payment.user_id == current_user.id)
        .order_by(Payment.created_at.desc())
    )
    return result.scalars().all()


# ── Helper ──────────────────────────────────────────────────────────────────

async def _update_payment(db: AsyncSession, token: str, new_status: str):
    result = await db.execute(
        select(Payment).where(Payment.provider_reference == token)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        return None, None

    payment.status = new_status
    if new_status == "paid":
        payment.paid_at = datetime.utcnow()
    await db.commit()

    user_result = await db.execute(select(User).where(User.id == payment.user_id))
    user = user_result.scalar_one_or_none()
    return user, payment
