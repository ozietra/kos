import uuid
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, field_validator
from typing import Any


# ─── AUTH ───────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Şifre en az 8 karakter olmalıdır.")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: str | None
    phone: str | None
    plan: str
    credits: int
    is_admin: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Şifre en az 8 karakter olmalıdır.")
        return v


# ─── BUSINESS ───────────────────────────────────────────────────────────────

class BusinessCreate(BaseModel):
    business_name: str
    nace_code: str | None = None
    nace_description: str | None = None
    founding_date: date | None = None
    employee_count: int | None = None
    annual_revenue: int | None = None
    city: str | None = None
    is_woman_entrepreneur: bool = False
    is_young_entrepreneur: bool = False
    is_disabled: bool = False
    is_veteran: bool = False
    tax_number: str | None = None  # will be encrypted before storage
    sector_description: str | None = None
    kosgeb_registered: bool = False
    has_recent_partnership: bool = False


class BusinessUpdate(BusinessCreate):
    business_name: str | None = None


class BusinessResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    business_name: str
    nace_code: str | None
    nace_description: str | None
    founding_date: date | None
    employee_count: int | None
    annual_revenue: int | None
    city: str | None
    is_woman_entrepreneur: bool
    is_young_entrepreneur: bool
    is_disabled: bool
    is_veteran: bool
    sector_description: str | None
    kosgeb_registered: bool
    has_recent_partnership: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── ELIGIBILITY ─────────────────────────────────────────────────────────────

class EligibleProgram(BaseModel):
    program_id: str
    program_name: str
    max_amount: int
    support_type: str
    key_requirements: list[str]
    next_step: str
    application_deadline: date | None


class IneligibleProgram(BaseModel):
    program_name: str
    reason: str
    could_be_eligible_if: str | None


class EligibilityWarning(BaseModel):
    type: str  # critical, warning, info
    message: str


class EligibilityResult(BaseModel):
    business_id: uuid.UUID
    eligible: list[EligibleProgram]
    ineligible: list[IneligibleProgram]
    warnings: list[EligibilityWarning]


# ─── NACE ────────────────────────────────────────────────────────────────────

class NaceSuggestRequest(BaseModel):
    description: str


class NaceCode(BaseModel):
    code: str
    description: str


class NaceSuggestResponse(BaseModel):
    nace_code: str
    nace_description: str
    is_kosgeb_eligible: bool
    confidence: str  # high, medium, low
    alternative_codes: list[NaceCode]
    disclaimer: str = "Bu öneri bilgilendirme amaçlıdır. Mali müşavirinizle doğrulayın."


# ─── APPLICATION ─────────────────────────────────────────────────────────────

class ApplicationCreate(BaseModel):
    business_id: uuid.UUID
    program_type: str
    application_year: int | None = None
    application_period: int | None = None


class ApplicationInputSubmit(BaseModel):
    # Adım 1: Proje Fikri
    project_title: str | None = None
    project_idea: str | None = None
    problem_solved: str | None = None
    # Adım 2: Pazar
    target_market: str | None = None
    competitors: str | None = None
    competitive_advantage: str | None = None
    market_size: str | None = None
    # Adım 3: Finansal
    requested_amount: int | None = None
    budget_items: str | None = None  # JSON string of items
    revenue_target_year1: int | None = None
    employment_target: int | None = None
    # Adım 4: Zaman
    project_duration_months: int | None = None
    milestones: str | None = None


class ApplicationResponse(BaseModel):
    id: uuid.UUID
    business_id: uuid.UUID
    program_type: str | None
    status: str
    project_title: str | None
    project_summary: str | None
    business_plan: str | None
    financial_projection: str | None
    timeline: str | None
    budget_breakdown: Any | None
    document_checklist: Any | None
    pdf_url: str | None
    generation_progress: int
    generation_status_text: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─── PROGRAMS ────────────────────────────────────────────────────────────────

class ProgramResponse(BaseModel):
    id: uuid.UUID
    program_name: str
    program_code: str | None
    max_support_amount: int | None
    support_type: str | None
    min_business_age_months: int | None
    max_business_age_months: int | None
    application_period_start: date | None
    application_period_end: date | None
    required_documents: list[str] | None
    key_criteria: list[str] | None
    is_active: bool
    last_updated: datetime

    model_config = {"from_attributes": True}


# ─── COMMON ──────────────────────────────────────────────────────────────────

class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str


# ─── PAYMENT ─────────────────────────────────────────────────────────────────

class CheckoutRequest(BaseModel):
    application_id: uuid.UUID
    plan: str = "starter"   # starter | pro
    provider: str = "iyzico"  # iyzico | paytr

    @field_validator("provider")
    @classmethod
    def valid_provider(cls, v: str) -> str:
        if v not in ("iyzico", "paytr"):
            raise ValueError("Geçersiz ödeme sağlayıcısı.")
        return v


class PaymentResponse(BaseModel):
    id: uuid.UUID
    plan: str
    amount: float
    currency: str
    status: str
    created_at: datetime
    paid_at: datetime | None

    model_config = {"from_attributes": True}
