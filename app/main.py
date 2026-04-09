from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.db.session import get_session_factory, init_db
from app.services.users import seed_default_admin


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    with get_session_factory()() as session:
        seed_default_admin(session)
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
        lifespan=lifespan,
        description=(
            "Reusable FastAPI template with JWT authentication, role-based access control, "
            "centralized settings, and a test-friendly application structure."
        ),
    )
    application.include_router(api_router, prefix=settings.api_v1_prefix)
    return application


app = create_app()
