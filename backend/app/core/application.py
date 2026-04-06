from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

import sentry_sdk
import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from app.api.router import api_router
from app.auth.bootstrap import ensure_demo_auth_bootstrap
from app.auth.turnstile import CloudflareTurnstileVerifier
from app.auth.verifiers import AuthenticationError, build_token_verifier
from app.core.config import Settings, get_settings
from app.core.db.session import DatabaseSessionManager
from app.core.llm.providers import NoopLLMProvider
from app.core.logging import configure_logging
from app.core.storage import LocalDebugStorageProvider, TenantScopedStorage
from app.core.tasks import create_celery_app

logger = structlog.get_logger(__name__)

PUBLIC_PATH_EXACT = {"/", "/openapi.json", "/v1/auth/login"}
PUBLIC_PATH_PREFIXES = ("/docs", "/redoc", "/v1/health")


def create_application(
    *,
    settings: Settings | None = None,
    db_session_manager: DatabaseSessionManager | None = None,
) -> FastAPI:
    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings)

    if resolved_settings.sentry_dsn:
        sentry_sdk.init(
            dsn=resolved_settings.sentry_dsn,
            environment=resolved_settings.environment.value,
            traces_sample_rate=0.1,
        )

    resolved_db_session_manager = db_session_manager or DatabaseSessionManager(
        resolved_settings.database_url,
        echo=resolved_settings.debug,
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        await ensure_demo_auth_bootstrap(
            settings=resolved_settings,
            db_session_manager=resolved_db_session_manager,
        )
        yield
        await resolved_db_session_manager.dispose()

    app = FastAPI(
        title=resolved_settings.app_name,
        debug=resolved_settings.debug,
        lifespan=lifespan,
    )
    app.state.settings = resolved_settings
    app.state.db_session_manager = resolved_db_session_manager
    app.state.token_verifier = build_token_verifier(resolved_settings)
    app.state.turnstile_verifier = CloudflareTurnstileVerifier(resolved_settings)
    app.state.celery_app = create_celery_app(resolved_settings)
    app.state.storage = TenantScopedStorage(provider=LocalDebugStorageProvider())
    app.state.llm_provider = NoopLLMProvider()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def attach_request_context(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if _is_public_path(request.url.path):
            return await call_next(request)

        try:
            context = await request.app.state.token_verifier.verify_request(request)
        except AuthenticationError as exc:
            return JSONResponse(status_code=401, content={"detail": str(exc)})

        request.state.request_context = context
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            institution_id=str(context.institution_id),
            user_id=str(context.user_id),
            role=context.role.value,
        )

        try:
            response = await call_next(request)
        finally:
            structlog.contextvars.clear_contextvars()

        response.headers["X-PrepareMe-Institution-Id"] = str(context.institution_id)
        return response

    @app.get("/", tags=["system"])
    async def root() -> dict[str, str]:
        return {"name": resolved_settings.app_name, "status": "booted"}

    app.include_router(api_router, prefix=resolved_settings.api_v1_prefix)

    logger.info(
        "application.created",
        environment=resolved_settings.environment.value,
        auth_mode=resolved_settings.auth_mode.value,
    )
    return app


def _is_public_path(path: str) -> bool:
    if path in PUBLIC_PATH_EXACT:
        return True
    return any(path == prefix or path.startswith(f"{prefix}/") for prefix in PUBLIC_PATH_PREFIXES)
