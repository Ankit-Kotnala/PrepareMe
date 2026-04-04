from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.core.config import Settings

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: str
    environment: str


@router.get("/liveness", response_model=HealthResponse)
async def liveness(request: Request) -> HealthResponse:
    settings: Settings = request.app.state.settings
    return HealthResponse(status="ok", environment=settings.environment.value)


@router.get("/readiness", response_model=HealthResponse)
async def readiness(request: Request) -> HealthResponse:
    settings: Settings = request.app.state.settings
    return HealthResponse(status="ready", environment=settings.environment.value)

