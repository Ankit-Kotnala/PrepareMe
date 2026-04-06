from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

import structlog
from sqlalchemy import select
from sqlalchemy.exc import OperationalError, ProgrammingError

from app.auth.security import hash_password
from app.core.config import Settings
from app.core.db.models import Institution, LocalAuthCredential, TenantPolicy, User
from app.core.db.session import DatabaseSessionManager
from app.core.enums import AnswerStrictness, AuthMode, ExplanationDepth, PlanTier, UserRole

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True)
class DemoUserSeed:
    email: str
    password: str
    name: str
    role: UserRole


DEMO_INSTITUTION_NAME = "PrepareMe Demo Academy"
DEMO_INSTITUTION_SLUG = "prepareme-demo"
DEMO_USERS: tuple[DemoUserSeed, ...] = (
    DemoUserSeed(
        email="admin@prepareme.local",
        password="Admin@123",
        name="Ananya Admin",
        role=UserRole.INSTITUTION_ADMIN,
    ),
    DemoUserSeed(
        email="teacher@prepareme.local",
        password="Teacher@123",
        name="Tarun Teacher",
        role=UserRole.TEACHER,
    ),
    DemoUserSeed(
        email="student@prepareme.local",
        password="Student@123",
        name="Sana Student",
        role=UserRole.STUDENT,
    ),
)


async def ensure_demo_auth_bootstrap(
    *,
    settings: Settings,
    db_session_manager: DatabaseSessionManager,
) -> None:
    if settings.auth_mode != AuthMode.LOCAL_JWT or not settings.bootstrap_demo_data:
        return

    try:
        institution = await _ensure_demo_institution(db_session_manager)
        await _ensure_demo_users_and_policy(
            db_session_manager=db_session_manager,
            institution_id=institution.id,
        )
    except (OperationalError, ProgrammingError) as exc:
        logger.warning(
            "auth.bootstrap.skipped",
            reason="database_not_ready",
            detail=str(exc),
        )
    except Exception:
        logger.exception("auth.bootstrap.failed")


async def _ensure_demo_institution(
    db_session_manager: DatabaseSessionManager,
) -> Institution:
    async with db_session_manager.session() as session:
        result = await session.execute(
            select(Institution).where(Institution.slug == DEMO_INSTITUTION_SLUG),
        )
        institution = result.scalar_one_or_none()
        if institution is not None:
            return institution

        institution = Institution(
            id=uuid4(),
            name=DEMO_INSTITUTION_NAME,
            slug=DEMO_INSTITUTION_SLUG,
            plan_tier=PlanTier.PROFESSIONAL,
            settings={"timezone": "Asia/Calcutta", "language": "en-IN"},
        )
        session.add(institution)
        await session.commit()
        await session.refresh(institution)
        logger.info("auth.bootstrap.institution_created", institution_id=str(institution.id))
        return institution


async def _ensure_demo_users_and_policy(
    *,
    db_session_manager: DatabaseSessionManager,
    institution_id: UUID,
) -> None:
    async with db_session_manager.session(institution_id) as session:
        existing_users_result = await session.execute(
            select(User).where(User.institution_id == institution_id),
        )
        existing_users = {
            user.email.lower(): user for user in existing_users_result.scalars().all()
        }
        existing_credentials_result = await session.execute(
            select(LocalAuthCredential).where(
                LocalAuthCredential.institution_id == institution_id,
            ),
        )
        existing_credentials = {
            credential.user_id: credential
            for credential in existing_credentials_result.scalars().all()
        }

        created_admin_user_id: UUID | None = None

        for demo_user in DEMO_USERS:
            user = existing_users.get(demo_user.email.lower())
            if user is None:
                user = User(
                    id=uuid4(),
                    institution_id=institution_id,
                    email=demo_user.email,
                    role=demo_user.role,
                    profile={"name": demo_user.name},
                )
                session.add(user)
                await session.flush()
                logger.info(
                    "auth.bootstrap.user_created",
                    institution_id=str(institution_id),
                    email=demo_user.email,
                    role=demo_user.role.value,
                )

            if user.id not in existing_credentials:
                credential = LocalAuthCredential(
                    id=uuid4(),
                    institution_id=institution_id,
                    user_id=user.id,
                    password_hash=hash_password(demo_user.password),
                )
                session.add(credential)
                existing_credentials[user.id] = credential

            if demo_user.role == UserRole.INSTITUTION_ADMIN:
                created_admin_user_id = user.id

        if created_admin_user_id is None:
            admin_user = next(
                (user for user in existing_users.values() if user.role == UserRole.INSTITUTION_ADMIN),
                None,
            )
            created_admin_user_id = admin_user.id if admin_user is not None else None

        policy_result = await session.execute(
            select(TenantPolicy).where(TenantPolicy.institution_id == institution_id),
        )
        policy = policy_result.scalar_one_or_none()
        if policy is None:
            policy = TenantPolicy(
                id=uuid4(),
                institution_id=institution_id,
                answer_strictness=AnswerStrictness.STRICT,
                min_confidence_threshold=0.75,
                content_approval_required=True,
                explanation_depth=ExplanationDepth.STANDARD,
                language="en-IN",
                custom_rules={"demo_mode": True},
                updated_by=created_admin_user_id,
            )
            session.add(policy)
            logger.info(
                "auth.bootstrap.policy_created",
                institution_id=str(institution_id),
            )

        await session.commit()
