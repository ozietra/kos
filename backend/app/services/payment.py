"""
iyzico Ödeme Servisi
Sandbox ve production modunu .env'den okur.
"""
import hashlib
import hmac
import json
import uuid
from datetime import datetime

import httpx
from app.config import settings


IYZICO_BASE_SANDBOX = "https://sandbox-api.iyzipay.com"
IYZICO_BASE_PROD    = "https://api.iyzipay.com"


def _base_url() -> str:
    return IYZICO_BASE_SANDBOX if settings.IYZICO_SANDBOX else IYZICO_BASE_PROD


def _random_header(api_key: str, secret_key: str, body: str) -> str:
    """
    iyzico Authorization header hesapla.
    Format: IYZWSv2 base64(api_key:random:hmac_sha256(api_key+random+body))
    """
    import base64
    import secrets
    random_key = secrets.token_hex(4)   # 8 char hex
    # HMAC-SHA256
    data = api_key + random_key + body
    signature = hmac.new(
        secret_key.encode("utf-8"),
        data.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    raw = f"{api_key}:{random_key}:{signature}"
    encoded = base64.b64encode(raw.encode()).decode()
    return f"IYZWSv2 {encoded}"


async def create_checkout_form(
    *,
    user_id: str,
    user_email: str,
    user_name: str,
    plan: str,             # "starter" | "pro"
    application_id: str,
    ip_address: str = "85.34.78.112",
) -> dict:
    """
    iyzico Başlangıç Ödeme Formu (Hosted Checkout).
    Dönüş: { checkoutFormContent, paymentPageUrl, token }
    """
    api_key    = settings.IYZICO_API_KEY
    secret_key = settings.IYZICO_SECRET_KEY
    price      = "499.00" if plan == "starter" else "999.00"

    payload = {
        "locale": "tr",
        "conversationId": application_id,
        "price": price,
        "paidPrice": price,
        "currency": "TRY",
        "basketId": application_id,
        "paymentGroup": "PRODUCT",
        "callbackUrl": f"{settings.FRONTEND_URL}/odeme/sonuc",
        "enabledInstallments": [1, 2, 3],
        "buyer": {
            "id": user_id,
            "name": (user_name.split()[0] if user_name else "Kullanici"),
            "surname": (user_name.split()[-1] if user_name and " " in user_name else "-"),
            "gsmNumber": "+905000000000",
            "email": user_email,
            "identityNumber": "11111111111",    # sandbox için
            "registrationAddress": "Türkiye",
            "ip": ip_address,
            "city": "Istanbul",
            "country": "Turkey",
        },
        "shippingAddress": {
            "contactName": user_name or "Kullanici",
            "city": "Istanbul",
            "country": "Turkey",
            "address": "Türkiye",
        },
        "billingAddress": {
            "contactName": user_name or "Kullanici",
            "city": "Istanbul",
            "country": "Turkey",
            "address": "Türkiye",
        },
        "basketItems": [
            {
                "id": plan,
                "name": f"kosgebhibe.com {plan.capitalize()} Planı",
                "category1": "Dijital Hizmet",
                "itemType": "VIRTUAL",
                "price": price,
            }
        ],
    }

    body_str = json.dumps(payload, ensure_ascii=False)
    headers = {
        "Authorization": _random_header(api_key, secret_key, body_str),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            f"{_base_url()}/payment/iyzipos/checkoutform/initialize/auth/ecom",
            content=body_str,
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()


async def retrieve_checkout_result(token: str) -> dict:
    """
    Ödeme sonucunu iyzico'dan doğrula.
    Webhook gelene kadar güvenilir kaynak olarak kullanılır.
    """
    api_key    = settings.IYZICO_API_KEY
    secret_key = settings.IYZICO_SECRET_KEY

    payload  = {"locale": "tr", "token": token}
    body_str = json.dumps(payload, ensure_ascii=False)
    headers  = {
        "Authorization": _random_header(api_key, secret_key, body_str),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            f"{_base_url()}/payment/iyzipos/checkoutform/auth/ecom/detail",
            content=body_str,
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()
