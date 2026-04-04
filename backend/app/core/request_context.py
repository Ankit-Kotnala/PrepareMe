from dataclasses import dataclass, field
from uuid import UUID

from app.core.enums import UserRole
from app.core.types import JSONValue


@dataclass(slots=True)
class RequestContext:
    institution_id: UUID
    user_id: UUID
    role: UserRole
    email: str | None = None
    session_id: str | None = None
    raw_claims: dict[str, JSONValue] = field(default_factory=dict)

    @property
    def is_staff(self) -> bool:
        return self.role in {
            UserRole.TEACHER,
            UserRole.COURSE_ADMIN,
            UserRole.INSTITUTION_ADMIN,
            UserRole.PLATFORM_ADMIN,
        }

