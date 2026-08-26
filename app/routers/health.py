from datetime import datetime
from fastapi import APIRouter
from app.models import HealthResponse

router = APIRouter(prefix="", tags=["health"])

APP_VERSION = "1.0.0"


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        version=APP_VERSION,
        timestamp=datetime.utcnow()
    )