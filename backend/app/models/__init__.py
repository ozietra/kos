import uuid
from datetime import datetime, date
from sqlalchemy import (
    String, Integer, BigInteger, Boolean, Text, Date,
    DateTime, ForeignKey, ARRAY, func
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(20))
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    plan: Mapped[str] = mapped_column(String(50), default="free")
    credits: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    reset_token: Mapped[str | None] = mapped_column(String(255))
    reset_token_expires: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    businesses: Mapped[list["Business"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    payments: Mapped[list["Payment"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    notification_subscriptions: Mapped[list["NotificationSubscription"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Business(Base):
    __tablename__ = "businesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    business_name: Mapped[str] = mapped_column(String(255), nullable=False)
    nace_code: Mapped[str | None] = mapped_column(String(10))
    nace_description: Mapped[str | None] = mapped_column(String(255))
    founding_date: Mapped[date | None] = mapped_column(Date)
    employee_count: Mapped[int | None] = mapped_column(Integer)
    annual_revenue: Mapped[int | None] = mapped_column(BigInteger)
    city: Mapped[str | None] = mapped_column(String(100))
    is_woman_entrepreneur: Mapped[bool] = mapped_column(Boolean, default=False)
    is_young_entrepreneur: Mapped[bool] = mapped_column(Boolean, default=False)
    is_disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    is_veteran: Mapped[bool] = mapped_column(Boolean, default=False)
    tax_number_encrypted: Mapped[str | None] = mapped_column(String(512))  # AES-256 encrypted
    sector_description: Mapped[str | None] = mapped_column(Text)
    kosgeb_registered: Mapped[bool] = mapped_column(Boolean, default=False)
    has_recent_partnership: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="businesses")
    eligibility_checks: Mapped[list["EligibilityCheck"]] = relationship(
        back_populates="business", cascade="all, delete-orphan"
    )
    applications: Mapped[list["Application"]] = relationship(
        back_populates="business", cascade="all, delete-orphan"
    )


class EligibilityCheck(Base):
    __tablename__ = "eligibility_checks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"))
    eligible_programs: Mapped[dict | None] = mapped_column(JSONB)
    ineligible_programs: Mapped[dict | None] = mapped_column(JSONB)
    warnings: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    business: Mapped["Business"] = relationship(back_populates="eligibility_checks")


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"))
    program_type: Mapped[str | None] = mapped_column(String(100))
    application_year: Mapped[int | None] = mapped_column(Integer)
    application_period: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50), default="draft")  # draft, generating, completed, paid
    project_title: Mapped[str | None] = mapped_column(String(255))
    project_summary: Mapped[str | None] = mapped_column(Text)
    business_plan: Mapped[str | None] = mapped_column(Text)
    financial_projection: Mapped[str | None] = mapped_column(Text)
    timeline: Mapped[str | None] = mapped_column(Text)
    budget_breakdown: Mapped[dict | None] = mapped_column(JSONB)
    document_checklist: Mapped[dict | None] = mapped_column(JSONB)
    pdf_url: Mapped[str | None] = mapped_column(String(500))
    payment_status: Mapped[str] = mapped_column(String(20), default="unpaid")  # unpaid | paid
    generation_progress: Mapped[int] = mapped_column(Integer, default=0)
    generation_status_text: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    business: Mapped["Business"] = relationship(back_populates="applications")
    inputs: Mapped[list["ApplicationInput"]] = relationship(
        back_populates="application", cascade="all, delete-orphan"
    )


class ApplicationInput(Base):
    __tablename__ = "application_inputs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("applications.id", ondelete="CASCADE")
    )
    field_name: Mapped[str] = mapped_column(String(100))
    field_value: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    application: Mapped["Application"] = relationship(back_populates="inputs")


class KosgebProgram(Base):
    __tablename__ = "kosgeb_programs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_name: Mapped[str] = mapped_column(String(255), nullable=False)
    program_code: Mapped[str | None] = mapped_column(String(50))
    max_support_amount: Mapped[int | None] = mapped_column(BigInteger)
    support_type: Mapped[str | None] = mapped_column(String(50))  # hibe, kredi_faiz, karma
    eligible_nace_prefixes: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    min_business_age_months: Mapped[int | None] = mapped_column(Integer)
    max_business_age_months: Mapped[int | None] = mapped_column(Integer)
    application_period_start: Mapped[date | None] = mapped_column(Date)
    application_period_end: Mapped[date | None] = mapped_column(Date)
    required_documents: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    key_criteria: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    # KOSGEB detay sayfasından çekilen zengin içerik (AI ve site gösterimi için)
    purpose: Mapped[str | None] = mapped_column(Text)            # Amaç / tanım
    eligibility: Mapped[str | None] = mapped_column(Text)        # Kimler başvurabilir / şartlar
    support_items: Mapped[list[dict] | None] = mapped_column(JSONB)  # [{unsur, tutar, oran, sure}]
    detail_url: Mapped[str | None] = mapped_column(String(500))  # Kaynak detay sayfası
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class SiteContent(Base):
    """Düzenlenebilir site içeriği (hero rozeti override, istatistik değerleri)."""
    __tablename__ = "site_content"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    label: Mapped[str | None] = mapped_column(String(255))
    value: Mapped[str | None] = mapped_column(Text)
    group: Mapped[str] = mapped_column(String(50), default="stats")  # stats | hero
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class ProgramFetchLog(Base):
    """KOSGEB sitesinden her çekme denemesinin denetim kaydı."""
    __tablename__ = "program_fetch_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_url: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(20))  # success|fetch_failed|parse_failed|no_change
    http_status: Mapped[int | None] = mapped_column(Integer)
    raw_text: Mapped[str | None] = mapped_column(Text)
    error: Mapped[str | None] = mapped_column(Text)
    proposals_created: Mapped[int] = mapped_column(Integer, default=0)
    triggered_by: Mapped[str | None] = mapped_column(String(40))  # schedule | admin:<id>
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProgramUpdateProposal(Base):
    """Admin onayı bekleyen program değişikliği. Onaylanmadan canlıya yansımaz."""
    __tablename__ = "program_update_proposals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("kosgeb_programs.id", ondelete="SET NULL")
    )
    program_code: Mapped[str | None] = mapped_column(String(50))
    change_type: Mapped[str] = mapped_column(String(20))  # create | update | deactivate
    proposed_data: Mapped[dict | None] = mapped_column(JSONB)
    current_data: Mapped[dict | None] = mapped_column(JSONB)
    diff_summary: Mapped[dict | None] = mapped_column(JSONB)  # [{field, old, new}]
    source_url: Mapped[str | None] = mapped_column(String(500))
    raw_excerpt: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[str | None] = mapped_column(String(10))
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending|approved|rejected|superseded
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    review_note: Mapped[str | None] = mapped_column(Text)
    fetch_log_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("program_fetch_logs.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PricingPlan(Base):
    """Admin'den düzenlenebilir fiyat planı + kampanya/indirim."""
    __tablename__ = "pricing_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)  # starter, pro
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # kuruş cinsinden
    currency: Mapped[str] = mapped_column(String(8), default="TRY")
    campaign_price: Mapped[int | None] = mapped_column(Integer)  # kuruş; aktifse geçerli fiyat
    campaign_label: Mapped[str | None] = mapped_column(String(100))
    campaign_start: Mapped[date | None] = mapped_column(Date)
    campaign_end: Mapped[date | None] = mapped_column(Date)
    features: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    application_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("applications.id"))
    amount: Mapped[int | None] = mapped_column(Integer)  # kuruş cinsinden
    currency: Mapped[str] = mapped_column(String(8), default="TRY")
    plan: Mapped[str | None] = mapped_column(String(50))  # starter, pro
    product_type: Mapped[str | None] = mapped_column(String(50))  # starter, pro, subscription
    provider: Mapped[str | None] = mapped_column(String(20))  # iyzico | paytr
    provider_reference: Mapped[str | None] = mapped_column(String(255))  # token / merchant_oid
    iyzico_payment_id: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="payments")


class NotificationSubscription(Base):
    __tablename__ = "notification_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    notification_type: Mapped[str | None] = mapped_column(String(50))  # period_open, new_program
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="notification_subscriptions")
