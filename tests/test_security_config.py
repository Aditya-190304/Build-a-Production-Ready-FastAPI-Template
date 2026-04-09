import pytest
from pydantic import ValidationError

from app.core.config import Settings
from tests.constants import EXAMPLE_ADMIN_EMAIL, TEST_SECRET_KEY


def _clear_sensitive_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        "APP_DATABASE_URL",
        "APP_SECRET_KEY",
        "APP_DEFAULT_ADMIN_EMAIL",
        "APP_DEFAULT_ADMIN_PASSWORD",
        "APP_CORS_ALLOW_ORIGINS",
        "APP_CORS_ALLOW_CREDENTIALS",
    ):
        monkeypatch.delenv(key, raising=False)


def test_settings_require_secret_key_with_minimum_length(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_sensitive_env(monkeypatch)
    try:
        Settings(
            _env_file=None,
            APP_DATABASE_URL="sqlite+aiosqlite:///:memory:",
            APP_SECRET_KEY="short-secret",
        )
    except ValidationError as exc:
        assert "APP_SECRET_KEY must be at least 32 characters long." in str(exc)
    else:
        raise AssertionError("Expected a short secret key to fail validation.")


def test_settings_require_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_sensitive_env(monkeypatch)
    try:
        Settings(_env_file=None, APP_SECRET_KEY=TEST_SECRET_KEY)
    except ValidationError as exc:
        assert "APP_DATABASE_URL" in str(exc)
    else:
        raise AssertionError("Expected missing APP_DATABASE_URL to fail validation.")


def test_cors_configuration_rejects_wildcard_with_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_sensitive_env(monkeypatch)
    try:
        Settings(
            _env_file=None,
            APP_DATABASE_URL="sqlite+aiosqlite:///:memory:",
            APP_SECRET_KEY=TEST_SECRET_KEY,
            APP_CORS_ALLOW_ORIGINS="*",
            APP_CORS_ALLOW_CREDENTIALS=True,
        )
    except ValidationError as exc:
        assert "APP_CORS_ALLOW_ORIGINS cannot contain '*'" in str(exc)
    else:
        raise AssertionError("Expected wildcard origins with credentials enabled to fail.")


def test_admin_seed_settings_must_be_provided_together(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_sensitive_env(monkeypatch)
    try:
        Settings(
            _env_file=None,
            APP_DATABASE_URL="sqlite+aiosqlite:///:memory:",
            APP_SECRET_KEY=TEST_SECRET_KEY,
            APP_DEFAULT_ADMIN_EMAIL=EXAMPLE_ADMIN_EMAIL,
        )
    except ValidationError as exc:
        assert "must be provided together" in str(exc)
    else:
        raise AssertionError("Expected incomplete admin seed settings to fail validation.")
