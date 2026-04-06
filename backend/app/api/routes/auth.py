from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import RequestContextDep
from app.auth.security import create_access_token
from app.auth.services import authenticate_local_user, get_institution_by_slug
from app.core.config import Settings
from app.core.db.session import DatabaseSessionManager
from app.core.enums import UserRole
from app.core.request_context import RequestContext

router = APIRouter(prefix="/auth", tags=["auth"])


class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    institution_id: UUID
    role: UserRole
    email: str | None = None
    display_name: str | None = None
    institution_name: str | None = None
    institution_slug: str | None = None
    session_id: str | None = None

    @classmethod
    def from_context(cls, context: RequestContext) -> "CurrentUserResponse":
        return cls(
            user_id=context.user_id,
            institution_id=context.institution_id,
            role=context.role,
            email=context.email,
            display_name=context.display_name,
            institution_name=context.institution_name,
            institution_slug=context.institution_slug,
            session_id=context.session_id,
        )


class LoginRequest(BaseModel):
    institution_slug: str = Field(min_length=3, max_length=120)
    email: str = Field(min_length=5, max_length=320)
    password: str = Field(min_length=8, max_length=128)
    turnstile_token: str | None = Field(default=None, min_length=1, max_length=2048)


class LoginUserResponse(BaseModel):
    user_id: UUID
    institution_id: UUID
    institution_name: str
    institution_slug: str
    role: UserRole
    email: str
    display_name: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int
    redirect_path: str
    user: LoginUserResponse


def _dashboard_path_for_role(role: UserRole) -> str:
    if role == UserRole.STUDENT:
        return "/student"
    if role in {UserRole.INSTITUTION_ADMIN, UserRole.PLATFORM_ADMIN}:
        return "/admin"
    return "/teacher"


def _extract_client_ip(request: Request) -> str | None:
    forwarded_for = request.headers.get("cf-connecting-ip") or request.headers.get("x-forwarded-for")
    if isinstance(forwarded_for, str) and forwarded_for.strip():
        return forwarded_for.split(",", maxsplit=1)[0].strip()
    return request.client.host if request.client is not None else None


@router.get("/me", response_model=CurrentUserResponse)
async def me(context: RequestContextDep) -> CurrentUserResponse:
    return CurrentUserResponse.from_context(context)


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, request: Request) -> LoginResponse:
    settings: Settings = request.app.state.settings
    db_session_manager: DatabaseSessionManager = request.app.state.db_session_manager

    if settings.turnstile_enabled:
        if payload.turnstile_token is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Complete the Cloudflare security check and try again.",
            )

        verification_result = await request.app.state.turnstile_verifier.verify(
            token=payload.turnstile_token,
            remote_ip=_extract_client_ip(request),
        )
        if not verification_result.success:
            detail = "Security verification failed or expired. Please retry the challenge."
            if "internal-error" in verification_result.error_codes:
                detail = "Security verification service is unavailable right now. Please try again."
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    normalized_slug = payload.institution_slug.strip().lower()
    async with db_session_manager.session() as session:
        institution = await get_institution_by_slug(session, normalized_slug)

    if institution is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid institution code or credentials.",
        )

    async with db_session_manager.session(institution.id) as session:
        authenticated_user = await authenticate_local_user(
            session,
            institution_id=institution.id,
            institution_name=institution.name,
            institution_slug=institution.slug,
            email=payload.email,
            password=payload.password,
        )

    if authenticated_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid institution code or credentials.",
        )

    access_token, expires_in_seconds = create_access_token(
        settings=settings,
        user_id=str(authenticated_user.user_id),
        institution_id=str(authenticated_user.institution_id),
        institution_name=authenticated_user.institution_name,
        institution_slug=authenticated_user.institution_slug,
        role=authenticated_user.role,
        email=authenticated_user.email,
        display_name=authenticated_user.display_name,
    )

    return LoginResponse(
        access_token=access_token,
        expires_in_seconds=expires_in_seconds,
        redirect_path=_dashboard_path_for_role(authenticated_user.role),
        user=LoginUserResponse(
            user_id=authenticated_user.user_id,
            institution_id=authenticated_user.institution_id,
            institution_name=authenticated_user.institution_name,
            institution_slug=authenticated_user.institution_slug,
            role=authenticated_user.role,
            email=authenticated_user.email,
            display_name=authenticated_user.display_name,
        ),
    )

