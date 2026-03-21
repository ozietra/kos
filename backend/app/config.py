from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "kosgebhibe"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 saat

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://kosgebhibe:kosgebhibe123@localhost:5432/kosgebhibe"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # iyzico
    IYZICO_API_KEY: str = ""
    IYZICO_SECRET_KEY: str = ""
    IYZICO_SANDBOX: bool = True  # False = production
    IYZICO_BASE_URL: str = "https://sandbox-api.iyzipay.com"

    # Email (Postal SMTP)
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""         # aısmtplib için
    SMTP_PASSWORD: str = ""     # eski ad — geriye dönük uyumluluk
    SMTP_FROM: str = "noreply@kosgebhibe.com"
    FROM_EMAIL: str = "noreply@kosgebhibe.com"
    FROM_NAME: str = "kosgebhibe.com"

    # Ödeme zorunlu mu? (test modunda False yaparak geçilebilir)
    PAYMENT_REQUIRED: bool = True

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # Encryption key for sensitive fields (AES-256)
    ENCRYPTION_KEY: str = "change-me-32-bytes-encryption!!!"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
