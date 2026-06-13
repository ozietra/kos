"""
PayTR Ödeme Servisi (iFrame API).

Akış:
1. create_payment_token() → PayTR'den iframe token alır.
2. Frontend, https://www.paytr.com/odeme/guvenli/{token} adresini iframe'de açar.
3. Ödeme sonrası PayTR, callback URL'ine bildirim POST eder.
4. verify_callback() hash'i doğrular; sunucu "OK" yanıtı döndürmelidir.

Doküman: https://www.paytr.com/entegrasyon/iframe-api
"""
import base64
import hashlib
import hmac
import json

import httpx

from app.config import settings

PAYTR_TOKEN_URL = "https://www.paytr.com/odeme/api/get-token"
PAYTR_IFRAME_URL = "https://www.paytr.com/odeme/guvenli/"


def _hmac_b64(message: str) -> str:
    digest = hmac.new(
        settings.PAYTR_MERCHANT_KEY.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return base64.b64encode(digest).decode("utf-8")


async def create_payment_token(
    *,
    merchant_oid: str,        # benzersiz sipariş no (harf+rakam, _ yok tercihen)
    user_email: str,
    amount_kurus: int,        # ödenecek tutar — kuruş
    user_name: str,
    plan_name: str,
    user_ip: str = "0.0.0.0",
) -> dict:
    """PayTR iframe token'ı al. Dönüş: {status, token | reason}."""
    test_mode = "1" if settings.PAYTR_SANDBOX else "0"
    no_installment = "0"
    max_installment = "0"
    currency = "TL"
    merchant_id = settings.PAYTR_MERCHANT_ID

    basket = [[plan_name, f"{amount_kurus / 100:.2f}", 1]]
    user_basket = base64.b64encode(
        json.dumps(basket, ensure_ascii=False).encode("utf-8")
    ).decode("utf-8")

    # PayTR token hash sırası (resmi dokümana göre)
    hash_str = (
        f"{merchant_id}{user_ip}{merchant_oid}{user_email}{amount_kurus}"
        f"{user_basket}{no_installment}{max_installment}{currency}{test_mode}"
    )
    paytr_token = _hmac_b64(hash_str + settings.PAYTR_MERCHANT_SALT)

    payload = {
        "merchant_id": merchant_id,
        "user_ip": user_ip,
        "merchant_oid": merchant_oid,
        "email": user_email,
        "payment_amount": str(amount_kurus),
        "paytr_token": paytr_token,
        "user_basket": user_basket,
        "debug_on": "1" if settings.PAYTR_SANDBOX else "0",
        "no_installment": no_installment,
        "max_installment": max_installment,
        "user_name": user_name or "Kullanici",
        "user_address": "Türkiye",
        "user_phone": "05000000000",
        "merchant_ok_url": f"{settings.FRONTEND_URL}/odeme/basarili",
        "merchant_fail_url": f"{settings.FRONTEND_URL}/odeme/basarisiz",
        "timeout_limit": "30",
        "currency": currency,
        "test_mode": test_mode,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(PAYTR_TOKEN_URL, data=payload)
        resp.raise_for_status()
        return resp.json()


def iframe_url(token: str) -> str:
    return f"{PAYTR_IFRAME_URL}{token}"


def verify_callback(form: dict) -> bool:
    """PayTR callback hash'ini doğrula."""
    merchant_oid = form.get("merchant_oid", "")
    status = form.get("status", "")
    total_amount = form.get("total_amount", "")
    received_hash = form.get("hash", "")

    hash_str = f"{merchant_oid}{settings.PAYTR_MERCHANT_SALT}{status}{total_amount}"
    expected = _hmac_b64(hash_str)
    return hmac.compare_digest(expected, received_hash)
