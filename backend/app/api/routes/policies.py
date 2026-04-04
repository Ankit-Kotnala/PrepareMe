from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import DbSessionDep, RequestContextDep, require_roles
from app.core.enums import UserRole
from app.policies.schemas import TenantPolicyResponse
from app.policies.services import get_tenant_policy, get_tenant_policy_by_id

router = APIRouter(prefix="/policies", tags=["policies"])

POLICY_ROLES = (
    UserRole.TEACHER,
    UserRole.COURSE_ADMIN,
    UserRole.INSTITUTION_ADMIN,
    UserRole.PLATFORM_ADMIN,
)


@router.get(
    "/me",
    response_model=TenantPolicyResponse,
    dependencies=[Depends(require_roles(*POLICY_ROLES))],
)
async def read_my_policy(
    db: DbSessionDep,
    context: RequestContextDep,
) -> TenantPolicyResponse:
    policy = await get_tenant_policy(db, context.institution_id)
    if policy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tenant policy configured for this institution.",
        )
    return TenantPolicyResponse.model_validate(policy)


@router.get(
    "/{policy_id}",
    response_model=TenantPolicyResponse,
    dependencies=[Depends(require_roles(*POLICY_ROLES))],
)
async def read_policy_by_id(
    policy_id: UUID,
    db: DbSessionDep,
    context: RequestContextDep,
) -> TenantPolicyResponse:
    policy = await get_tenant_policy_by_id(db, context.institution_id, policy_id)
    if policy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant policy not found.",
        )
    return TenantPolicyResponse.model_validate(policy)

