"""phase0 foundation schema

Revision ID: 20260405_0001
Revises:
Create Date: 2026-04-05 02:10:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260405_0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


plan_tier = postgresql.ENUM(
    "starter",
    "professional",
    "enterprise",
    name="plan_tier",
    create_type=False,
)
user_role = postgresql.ENUM(
    "student",
    "teacher",
    "course_admin",
    "institution_admin",
    "platform_admin",
    name="user_role",
    create_type=False,
)
answer_strictness = postgresql.ENUM(
    "strict",
    "standard",
    "open",
    name="answer_strictness",
    create_type=False,
)
explanation_depth = postgresql.ENUM(
    "concise",
    "standard",
    "detailed",
    name="explanation_depth",
    create_type=False,
)
ai_response_type = postgresql.ENUM(
    "answer",
    "hedge",
    "refusal",
    "redirect",
    name="ai_response_type",
    create_type=False,
)


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS ltree")
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'vector') THEN
                CREATE EXTENSION IF NOT EXISTS vector;
            END IF;
        END
        $$;
        """
    )

    bind = op.get_bind()
    plan_tier.create(bind, checkfirst=True)
    user_role.create(bind, checkfirst=True)
    answer_strictness.create(bind, checkfirst=True)
    explanation_depth.create(bind, checkfirst=True)
    ai_response_type.create(bind, checkfirst=True)

    op.create_table(
        "institutions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("plan_tier", plan_tier, nullable=False, server_default="starter"),
        sa.Column("settings", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("timezone('utc', now())")),
        sa.UniqueConstraint("slug", name="uq_institutions_slug"),
    )
    op.create_index("ix_institutions_slug", "institutions", ["slug"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institution_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("profile", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("timezone('utc', now())")),
        sa.UniqueConstraint("institution_id", "email", name="uq_users_institution_id_email"),
    )
    op.create_index("ix_users_institution_id", "users", ["institution_id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    op.create_table(
        "tenant_policies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institution_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("answer_strictness", answer_strictness, nullable=False, server_default="standard"),
        sa.Column("min_confidence_threshold", sa.Float(), nullable=False, server_default="0.6"),
        sa.Column("content_approval_required", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("explanation_depth", explanation_depth, nullable=False, server_default="standard"),
        sa.Column("language", sa.String(length=32), nullable=False, server_default="en-IN"),
        sa.Column("custom_rules", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("timezone('utc', now())")),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.UniqueConstraint("institution_id", name="uq_tenant_policies_institution_id"),
    )
    op.create_index("ix_tenant_policies_institution_id", "tenant_policies", ["institution_id"], unique=False)

    op.create_table(
        "ai_interactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("institution_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("session_id", sa.String(length=255), nullable=True),
        sa.Column("query", sa.Text(), nullable=False),
        sa.Column("retrieved_chunks", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("confidence_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("response", sa.Text(), nullable=False),
        sa.Column("response_type", ai_response_type, nullable=False),
        sa.Column("curriculum_node_ids", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("policy_config_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("latency_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("model_used", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("timezone('utc', now())")),
    )
    op.create_index("ix_ai_interactions_institution_id", "ai_interactions", ["institution_id"], unique=False)
    op.create_index("ix_ai_interactions_user_id", "ai_interactions", ["user_id"], unique=False)

    op.execute(
        """
        CREATE OR REPLACE FUNCTION prevent_ai_interactions_mutation()
        RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION 'ai_interactions is immutable and append-only';
        END;
        $$ LANGUAGE plpgsql
        """
    )
    op.execute(
        """
        CREATE TRIGGER ai_interactions_no_update
        BEFORE UPDATE ON ai_interactions
        FOR EACH ROW
        EXECUTE FUNCTION prevent_ai_interactions_mutation()
        """
    )
    op.execute(
        """
        CREATE TRIGGER ai_interactions_no_delete
        BEFORE DELETE ON ai_interactions
        FOR EACH ROW
        EXECUTE FUNCTION prevent_ai_interactions_mutation()
        """
    )

    for table_name in ("users", "tenant_policies", "ai_interactions"):
        op.execute(f"ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY")
        op.execute(
            f"""
            CREATE POLICY {table_name}_tenant_isolation
            ON {table_name}
            USING (
                institution_id = NULLIF(current_setting('app.institution_id', true), '')::uuid
            )
            WITH CHECK (
                institution_id = NULLIF(current_setting('app.institution_id', true), '')::uuid
            )
            """
        )


def downgrade() -> None:
    for table_name in ("ai_interactions", "tenant_policies", "users"):
        op.execute(f"DROP POLICY IF EXISTS {table_name}_tenant_isolation ON {table_name}")

    op.execute("DROP TRIGGER IF EXISTS ai_interactions_no_delete ON ai_interactions")
    op.execute("DROP TRIGGER IF EXISTS ai_interactions_no_update ON ai_interactions")
    op.execute("DROP FUNCTION IF EXISTS prevent_ai_interactions_mutation")

    op.drop_index("ix_ai_interactions_user_id", table_name="ai_interactions")
    op.drop_index("ix_ai_interactions_institution_id", table_name="ai_interactions")
    op.drop_table("ai_interactions")

    op.drop_index("ix_tenant_policies_institution_id", table_name="tenant_policies")
    op.drop_table("tenant_policies")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_institution_id", table_name="users")
    op.drop_table("users")

    op.drop_index("ix_institutions_slug", table_name="institutions")
    op.drop_table("institutions")

    bind = op.get_bind()
    ai_response_type.drop(bind, checkfirst=True)
    explanation_depth.drop(bind, checkfirst=True)
    answer_strictness.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)
    plan_tier.drop(bind, checkfirst=True)

