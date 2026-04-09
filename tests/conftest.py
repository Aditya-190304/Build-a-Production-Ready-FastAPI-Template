import asyncio
import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.db.session import get_engine, get_session_factory


@pytest.fixture
def client() -> Iterator[TestClient]:
    os.environ["APP_NAME"] = "FastAPI Template Test"
    os.environ["APP_ENV"] = "test"
    os.environ["APP_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    os.environ["APP_SECRET_KEY"] = "test-secret-key-with-at-least-32-bytes"
    os.environ["APP_DEFAULT_ADMIN_EMAIL"] = "aditi.admin@example.com"
    os.environ["APP_DEFAULT_ADMIN_PASSWORD"] = "AdminPass123!"

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    from app.main import create_app

    with TestClient(create_app()) as test_client:
        yield test_client

    asyncio.run(get_engine().dispose())
    get_session_factory.cache_clear()
    get_engine.cache_clear()
    get_settings.cache_clear()
