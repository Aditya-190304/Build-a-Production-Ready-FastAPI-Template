from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from app.core.config import get_settings

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    app_name: str
    environment: str
    version: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok",
                "app_name": "FastAPI Template",
                "environment": "local",
                "version": "0.1.0",
            }
        }
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description=(
        "Simple endpoint used for smoke checks and readiness probes. "
        "Returns service metadata along with the current environment."
    ),
)
def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        environment=settings.app_env,
        version=settings.version,
    )
