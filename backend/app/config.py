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

    # ── Yapay zekâ sağlayıcıları (sırayla denenir; biri limit/hata verince
    #    otomatik diğerine geçilir). Hepsi OpenAI-uyumlu; hepsi Llama-3.3-70B sunar.
    #    İstediğin kadar anahtar ekleyebilirsin — fazlası = daha çok kapasite. ──
    GROQ_API_KEY: str = ""                       # birincil Groq anahtarı
    GROQ_API_KEYS_EXTRA: str = ""                # virgülle ayrılmış ek Groq anahtarları
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "meta-llama/llama-3.3-70b-instruct"
    CEREBRAS_API_KEY: str = ""
    CEREBRAS_MODEL: str = "llama-3.3-70b"
    TOGETHER_API_KEY: str = ""
    TOGETHER_MODEL: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo"

    # iyzico
    IYZICO_API_KEY: str = ""
    IYZICO_SECRET_KEY: str = ""
    IYZICO_SANDBOX: bool = True  # False = production
    IYZICO_BASE_URL: str = "https://sandbox-api.iyzipay.com"

    # PayTR
    PAYTR_MERCHANT_ID: str = ""
    PAYTR_MERCHANT_KEY: str = ""
    PAYTR_MERCHANT_SALT: str = ""
    PAYTR_SANDBOX: bool = True

    # Varsayılan ödeme sağlayıcısı: paytr | iyzico
    DEFAULT_PAYMENT_PROVIDER: str = "iyzico"

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

    # İlk admin: bu e-postaya sahip mevcut kullanıcı başlangıçta admin yapılır
    ADMIN_EMAIL: str = ""

    # KOSGEB program oto-güncelleme
    KOSGEB_SCRAPE_ENABLED: bool = True
    KOSGEB_SCRAPE_CRON_DAY: str = "mon"   # APScheduler day_of_week
    KOSGEB_SCRAPE_CRON_HOUR: int = 4

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
