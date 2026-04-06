from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import AuthMode, Environment

TURNSTILE_TEST_SITE_KEY = "1x00000000000000000000AA"
TURNSTILE_TEST_SECRET_KEY = "1x0000000000000000000000000000000AA"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PREPAREME_",
        extra="ignore",
    )

    app_name: str = "PrepareMe API"
    environment: Environment = Environment.LOCAL
    debug: bool = False
    api_v1_prefix: str = "/v1"
    frontend_url: str = "http://localhost:3000"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5433/prepareme"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    auth_mode: AuthMode = AuthMode.TEST_HEADER
    auth_user_id_claim: str = "sub"
    auth_role_claim: str = "role"
    auth_institution_id_claim: str = "institution_id"
    auth_institution_name_claim: str = "institution_name"
    auth_institution_slug_claim: str = "institution_slug"
    auth_email_claim: str = "email"
    auth_display_name_claim: str = "name"
    auth_session_id_claim: str = "sid"
    auth_audience: str | None = None
    clerk_jwks_url: str | None = None
    clerk_issuer: str | None = None
    jwt_secret: str = "prepareme-local-dev-secret"
    jwt_algorithm: str = "HS256"
    jwt_issuer: str = "prepareme.local"
    jwt_access_token_expires_minutes: int = 60
    bootstrap_demo_data: bool = True
    turnstile_enabled: bool = True
    turnstile_site_key: str = TURNSTILE_TEST_SITE_KEY
    turnstile_secret_key: str = TURNSTILE_TEST_SECRET_KEY
    turnstile_expected_hostname: str | None = None
    turnstile_timeout_seconds: float = 5.0

    sentry_dsn: str | None = None
    log_level: str = "INFO"

    storage_bucket_name: str = "prepareme-dev"
    storage_region: str = "ap-south-1"

    @field_validator(
        "auth_audience",
        "clerk_jwks_url",
        "clerk_issuer",
        "turnstile_expected_hostname",
        "sentry_dsn",
        mode="before",
    )
    @classmethod
    def normalize_optional_strings(cls, value: str | None) -> str | None:
        if isinstance(value, str):
            stripped = value.strip()
            return stripped or None
        return value

    @field_validator("turnstile_site_key", mode="before")
    @classmethod
    def normalize_turnstile_site_key(cls, value: str | None) -> str:
        if isinstance(value, str):
            stripped = value.strip()
            if stripped:
                return stripped
        return TURNSTILE_TEST_SITE_KEY

    @field_validator("turnstile_secret_key", mode="before")
    @classmethod
    def normalize_turnstile_secret_key(cls, value: str | None) -> str:
        if isinstance(value, str):
            stripped = value.strip()
            if stripped:
                return stripped
        return TURNSTILE_TEST_SECRET_KEY

    @property
    def sync_database_url(self) -> str:
        if self.database_url.startswith("postgresql+asyncpg://"):
            return self.database_url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
        if self.database_url.startswith("sqlite+aiosqlite:///"):
            return self.database_url.replace("sqlite+aiosqlite:///", "sqlite+pysqlite:///", 1)
        return self.database_url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

