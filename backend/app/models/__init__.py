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
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    application_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("applications.id"))
    amount: Mapped[int | None] = mapped_column(Integer)  # kuruş cinsinden
    product_type: Mapped[str | None] = mapped_column(String(50))  # starter, pro, subscription
    iyzico_payment_id: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="pending")
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
