from collections.abc import AsyncIterator
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.auth.bootstrap import ensure_demo_auth_bootstrap
from app.core.application import create_application
from app.core.config import Settings
from app.core.db.base import Base
from app.core.db.session import DatabaseSessionManager
from app.core.enums import AuthMode, Environment


async def _build_test_application(
    *,
    auth_mode: AuthMode = AuthMode.TEST_HEADER,
    bootstrap_demo_data: bool = False,
    turnstile_enabled: bool = False,
) -> AsyncIterator:
    with TemporaryDirectory() as temp_dir:
        database_path = Path(temp_dir) / "prepareme-test.db"
        settings = Settings(
            app_name="PrepareMe Test API",
            environment=Environment.TEST,
            auth_mode=auth_mode,
            bootstrap_demo_data=bootstrap_demo_data,
            database_url=f"sqlite+aiosqlite:///{database_path.as_posix()}",
            redis_url="redis://localhost:6379/9",
            celery_broker_url="redis://localhost:6379/9",
            celery_result_backend="redis://localhost:6379/10",
            cors_origins=["http://localhost:3000"],
            jwt_secret="prepareme-test-secret-for-local-jwt-auth",
            jwt_issuer="prepareme.test",
            turnstile_enabled=turnstile_enabled,
        )
        db_session_manager = DatabaseSessionManager(settings.database_url)
        async with db_session_manager.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        application = create_application(
            settings=settings,
            db_session_manager=db_session_manager,
        )

        if bootstrap_demo_data:
            await ensure_demo_auth_bootstrap(
                settings=settings,
                db_session_manager=db_session_manager,
            )

        yield application

        await db_session_manager.dispose()


@pytest_asyncio.fixture
async def app() -> AsyncIterator:
    async for application in _build_test_application():
        yield application


@pytest_asyncio.fixture
async def local_auth_app() -> AsyncIterator:
    async for application in _build_test_application(
        auth_mode=AuthMode.LOCAL_JWT,
        bootstrap_demo_data=True,
    ):
        yield application


@pytest_asyncio.fixture
async def client(app) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        yield async_client


@pytest_asyncio.fixture
async def local_auth_client(local_auth_app) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=local_auth_app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as async_client:
        yield async_client

