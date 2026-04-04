from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from app.api.dependencies import RequestContextDep
from app.core.enums import UserRole
from app.core.request_context import RequestContext

router = APIRouter(prefix="/auth", tags=["auth"])


class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    institution_id: UUID
    role: UserRole
    email: str | None = None
    session_id: str | None = None

    @classmethod
    def from_context(cls, context: RequestContext) -> "CurrentUserResponse":
        return cls(
            user_id=context.user_id,
            institution_id=context.institution_id,
            role=context.role,
            email=context.email,
            session_id=context.session_id,
        )


@router.get("/me", response_model=CurrentUserResponse)
async def me(context: RequestContextDep) -> CurrentUserResponse:
    return CurrentUserResponse.from_context(context)

