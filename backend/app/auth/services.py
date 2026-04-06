from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import verify_password
from app.core.db.models import Institution, LocalAuthCredential, User
from app.core.enums import UserRole


@dataclass(slots=True)
class AuthenticatedUser:
    user_id: UUID
    institution_id: UUID
    institution_name: str
    institution_slug: str
    role: UserRole
    email: str
    display_name: str


async def get_institution_by_slug(
    db: AsyncSession,
    institution_slug: str,
) -> Institution | None:
    normalized_slug = institution_slug.strip().lower()
    result = await db.execute(
        select(Institution).where(func.lower(Institution.slug) == normalized_slug),
    )
    return result.scalar_one_or_none()


async def authenticate_local_user(
    db: AsyncSession,
    *,
    institution_id: UUID,
    institution_name: str,
    institution_slug: str,
    email: str,
    password: str,
) -> AuthenticatedUser | None:
    normalized_email = email.strip().lower()

    query: Select[tuple[User, LocalAuthCredential]] = select(User, LocalAuthCredential).join(
        LocalAuthCredential,
        LocalAuthCredential.user_id == User.id,
    ).where(
        User.institution_id == institution_id,
        LocalAuthCredential.institution_id == institution_id,
        func.lower(User.email) == normalized_email,
    )

    result = await db.execute(query)
    row = result.one_or_none()
    if row is None:
        return None

    user, credential = row
    if not verify_password(password, credential.password_hash):
        return None

    profile_name = user.profile.get("name") if isinstance(user.profile, dict) else None
    display_name = profile_name if isinstance(profile_name, str) else user.email

    return AuthenticatedUser(
        user_id=user.id,
        institution_id=user.institution_id,
        institution_name=institution_name,
        institution_slug=institution_slug,
        role=user.role,
        email=user.email,
        display_name=display_name,
    )

