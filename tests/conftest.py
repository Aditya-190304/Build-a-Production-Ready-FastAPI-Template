import asyncio
import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.db.session import get_engine, get_session_factory, init_db
from app.services.users import seed_default_admin
from tests.constants import (
    DEFAULT_CORS_ALLOW_HEADERS,
    DEFAULT_CORS_ALLOW_METHODS,
    DEFAULT_CORS_ALLOW_ORIGINS,
    EXAMPLE_ADMIN_EMAIL,
    TEST_ADMIN_PASSWORD,
    TEST_APP_NAME,
    TEST_DATABASE_URL,
    TEST_ENV,
    TEST_SECRET_KEY,
)


@pytest.fixture
def client() -> Iterator[TestClient]:
    os.environ["APP_NAME"] = TEST_APP_NAME
    os.environ["APP_ENV"] = TEST_ENV
    os.environ["APP_DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["APP_SECRET_KEY"] = TEST_SECRET_KEY
    os.environ["APP_CORS_ALLOW_ORIGINS"] = DEFAULT_CORS_ALLOW_ORIGINS
    os.environ["APP_CORS_ALLOW_CREDENTIALS"] = "true"
    os.environ["APP_CORS_ALLOW_METHODS"] = DEFAULT_CORS_ALLOW_METHODS
    os.environ["APP_CORS_ALLOW_HEADERS"] = DEFAULT_CORS_ALLOW_HEADERS
    os.environ["APP_DEFAULT_ADMIN_EMAIL"] = EXAMPLE_ADMIN_EMAIL
    os.environ["APP_DEFAULT_ADMIN_PASSWORD"] = TEST_ADMIN_PASSWORD

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    from app.main import create_app

    asyncio.run(init_db())

    async def bootstrap_admin() -> None:
        async with get_session_factory()() as session:
            await seed_default_admin(session)

    asyncio.run(bootstrap_admin())

    with TestClient(create_app()) as test_client:
        yield test_client

    asyncio.run(get_engine().dispose())
    get_session_factory.cache_clear()
    get_engine.cache_clear()
    get_settings.cache_clear()
