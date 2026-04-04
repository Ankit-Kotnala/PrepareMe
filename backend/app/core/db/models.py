from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.core.enums import AIResponseType, AnswerStrictness, ExplanationDepth, PlanTier, UserRole
from app.core.types import JSONValue


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Institution(Base):
    __tablename__ = "institutions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    plan_tier: Mapped[PlanTier] = mapped_column(
        SQLEnum(PlanTier, name="plan_tier"),
        nullable=False,
        default=PlanTier.STARTER,
    )
    settings: Mapped[dict[str, JSONValue]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
    )

    users: Mapped[list["User"]] = relationship(back_populates="institution")
    tenant_policy: Mapped["TenantPolicy | None"] = relationship(back_populates="institution")


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    institution_id: Mapped[UUID] = mapped_column(
        ForeignKey("institutions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name="user_role"), nullable=False)
    profile: Mapped[dict[str, JSONValue]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
    )

    institution: Mapped[Institution] = relationship(back_populates="users")


class TenantPolicy(Base):
    __tablename__ = "tenant_policies"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    institution_id: Mapped[UUID] = mapped_column(
        ForeignKey("institutions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    answer_strictness: Mapped[AnswerStrictness] = mapped_column(
        SQLEnum(AnswerStrictness, name="answer_strictness"),
        nullable=False,
        default=AnswerStrictness.STANDARD,
    )
    min_confidence_threshold: Mapped[float] = mapped_column(Float, nullable=False, default=0.6)
    content_approval_required: Mapped[bool] = mapped_column(nullable=False, default=True)
    explanation_depth: Mapped[ExplanationDepth] = mapped_column(
        SQLEnum(ExplanationDepth, name="explanation_depth"),
        nullable=False,
        default=ExplanationDepth.STANDARD,
    )
    language: Mapped[str] = mapped_column(String(32), nullable=False, default="en-IN")
    custom_rules: Mapped[dict[str, JSONValue]] = mapped_column(JSON, default=dict)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
    )
    updated_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    institution: Mapped[Institution] = relationship(back_populates="tenant_policy")
    updated_by_user: Mapped[User | None] = relationship()


class AIInteraction(Base):
    __tablename__ = "ai_interactions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    institution_id: Mapped[UUID] = mapped_column(
        ForeignKey("institutions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    session_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    retrieved_chunks: Mapped[list[JSONValue]] = mapped_column(JSON, default=list)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    response_type: Mapped[AIResponseType] = mapped_column(
        SQLEnum(AIResponseType, name="ai_response_type"),
        nullable=False,
    )
    curriculum_node_ids: Mapped[list[JSONValue]] = mapped_column(JSON, default=list)
    policy_config_snapshot: Mapped[dict[str, JSONValue]] = mapped_column(JSON, default=dict)
    latency_ms: Mapped[int] = mapped_column(nullable=False, default=0)
    model_used: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
    )

