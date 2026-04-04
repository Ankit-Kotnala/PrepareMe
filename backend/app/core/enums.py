from enum import Enum


class Environment(str, Enum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class AuthMode(str, Enum):
    TEST_HEADER = "test_header"
    CLERK = "clerk"


class PlanTier(str, Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    COURSE_ADMIN = "course_admin"
    INSTITUTION_ADMIN = "institution_admin"
    PLATFORM_ADMIN = "platform_admin"


class AnswerStrictness(str, Enum):
    STRICT = "strict"
    STANDARD = "standard"
    OPEN = "open"


class ExplanationDepth(str, Enum):
    CONCISE = "concise"
    STANDARD = "standard"
    DETAILED = "detailed"


class AIResponseType(str, Enum):
    ANSWER = "answer"
    HEDGE = "hedge"
    REFUSAL = "refusal"
    REDIRECT = "redirect"

