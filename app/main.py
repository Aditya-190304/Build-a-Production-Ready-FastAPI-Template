from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.error_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.core.logging.middleware import register_logging_middleware
from app.db.session import get_engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        yield
    finally:
        if get_engine.cache_info().currsize:
            await get_engine().dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings)

    application = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
        lifespan=lifespan,
        description=(
            "Reusable FastAPI template with JWT authentication, role-based access control, "
            "centralized settings, standardized error handling, structured logging, "
            "and a test-friendly application structure."
        ),
    )
    register_exception_handlers(application)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins_list,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods_list,
        allow_headers=settings.cors_allow_headers_list,
    )
    register_logging_middleware(application)
    application.include_router(api_router, prefix=settings.api_v1_prefix)
    return application


app = create_app()
