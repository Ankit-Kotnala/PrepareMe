from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models import TenantPolicy


async def get_tenant_policy(
    db: AsyncSession,
    institution_id: UUID,
) -> TenantPolicy | None:
    result = await db.execute(
        select(TenantPolicy).where(TenantPolicy.institution_id == institution_id),
    )
    return result.scalar_one_or_none()


async def get_tenant_policy_by_id(
    db: AsyncSession,
    institution_id: UUID,
    policy_id: UUID,
) -> TenantPolicy | None:
    result = await db.execute(
        select(TenantPolicy).where(
            TenantPolicy.institution_id == institution_id,
            TenantPolicy.id == policy_id,
        ),
    )
    return result.scalar_one_or_none()

