"""local auth credentials

Revision ID: 20260405_0002
Revises: 20260405_0001
Create Date: 2026-04-05 04:05:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260405_0002"
down_revision: str | None = "20260405_0001"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "local_auth_credentials",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "institution_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("institutions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("timezone('utc', now())"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("timezone('utc', now())"),
        ),
        sa.UniqueConstraint("user_id", name="uq_local_auth_credentials_user_id"),
    )
    op.create_index(
        "ix_local_auth_credentials_institution_id",
        "local_auth_credentials",
        ["institution_id"],
        unique=False,
    )
    op.create_index(
        "ix_local_auth_credentials_user_id",
        "local_auth_credentials",
        ["user_id"],
        unique=False,
    )

    op.execute("ALTER TABLE local_auth_credentials ENABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY local_auth_credentials_tenant_isolation
        ON local_auth_credentials
        USING (
            institution_id = NULLIF(current_setting('app.institution_id', true), '')::uuid
        )
        WITH CHECK (
            institution_id = NULLIF(current_setting('app.institution_id', true), '')::uuid
        )
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS local_auth_credentials_tenant_isolation ON local_auth_credentials"
    )
    op.drop_index("ix_local_auth_credentials_user_id", table_name="local_auth_credentials")
    op.drop_index("ix_local_auth_credentials_institution_id", table_name="local_auth_credentials")
    op.drop_table("local_auth_credentials")

