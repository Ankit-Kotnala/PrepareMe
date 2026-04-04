from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import AuthMode, Environment


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
    auth_email_claim: str = "email"
    auth_session_id_claim: str = "sid"
    auth_audience: str | None = None
    clerk_jwks_url: str | None = None
    clerk_issuer: str | None = None

    sentry_dsn: str | None = None
    log_level: str = "INFO"

    storage_bucket_name: str = "prepareme-dev"
    storage_region: str = "ap-south-1"

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

