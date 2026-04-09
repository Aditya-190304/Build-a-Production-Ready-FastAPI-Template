from functools import lru_cache

from pydantic import EmailStr, Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url

from app.core.constants import (
    API_V1_PREFIX_DEFAULT,
    APP_DEBUG_DEFAULT,
    APP_ENV_DEFAULT,
    APP_NAME_DEFAULT,
    APP_VERSION_DEFAULT,
    DEFAULT_CORS_ALLOW_CREDENTIALS,
    DEFAULT_CORS_ALLOW_HEADERS,
    DEFAULT_CORS_ALLOW_METHODS,
    DEFAULT_CORS_ALLOW_ORIGINS,
)


class Settings(BaseSettings):
    app_name: str = Field(default=APP_NAME_DEFAULT, validation_alias="APP_NAME")
    app_env: str = Field(default=APP_ENV_DEFAULT, validation_alias="APP_ENV")
    debug: bool = Field(default=APP_DEBUG_DEFAULT, validation_alias="APP_DEBUG")
    api_v1_prefix: str = Field(default=API_V1_PREFIX_DEFAULT, validation_alias="APP_API_V1_PREFIX")
    version: str = Field(default=APP_VERSION_DEFAULT, validation_alias="APP_VERSION")
    database_url: str = Field(..., validation_alias="APP_DATABASE_URL")
    db_pool_size: int = Field(default=10, validation_alias="APP_DB_POOL_SIZE")
    db_max_overflow: int = Field(default=20, validation_alias="APP_DB_MAX_OVERFLOW")
    db_pool_timeout: int = Field(default=30, validation_alias="APP_DB_POOL_TIMEOUT")
    db_pool_recycle: int = Field(default=1800, validation_alias="APP_DB_POOL_RECYCLE")
    secret_key: SecretStr = Field(..., validation_alias="APP_SECRET_KEY")
    access_token_expire_minutes: int = Field(
        default=30,
        validation_alias="APP_ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    cors_allow_origins: str = Field(
        default=DEFAULT_CORS_ALLOW_ORIGINS,
        validation_alias="APP_CORS_ALLOW_ORIGINS",
    )
    cors_allow_credentials: bool = Field(
        default=DEFAULT_CORS_ALLOW_CREDENTIALS,
        validation_alias="APP_CORS_ALLOW_CREDENTIALS",
    )
    cors_allow_methods: str = Field(
        default=DEFAULT_CORS_ALLOW_METHODS,
        validation_alias="APP_CORS_ALLOW_METHODS",
    )
    cors_allow_headers: str = Field(
        default=DEFAULT_CORS_ALLOW_HEADERS,
        validation_alias="APP_CORS_ALLOW_HEADERS",
    )
    default_admin_email: EmailStr | None = Field(
        default=None,
        validation_alias="APP_DEFAULT_ADMIN_EMAIL",
    )
    default_admin_password: SecretStr | None = Field(
        default=None,
        validation_alias="APP_DEFAULT_ADMIN_PASSWORD",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def sync_database_url(self) -> str:
        url = make_url(self.database_url)
        if url.drivername == "postgresql+asyncpg":
            return str(url.set(drivername="postgresql+psycopg"))
        if url.drivername == "sqlite+aiosqlite":
            return str(url.set(drivername="sqlite"))
        return str(url)

    @property
    def cors_allow_origins_list(self) -> list[str]:
        return _split_csv(self.cors_allow_origins)

    @property
    def cors_allow_methods_list(self) -> list[str]:
        return _split_csv(self.cors_allow_methods)

    @property
    def cors_allow_headers_list(self) -> list[str]:
        return _split_csv(self.cors_allow_headers)

    @model_validator(mode="after")
    def validate_security_settings(self) -> "Settings":
        secret_value = self.secret_key.get_secret_value()
        admin_password = (
            self.default_admin_password.get_secret_value()
            if self.default_admin_password is not None
            else None
        )

        if self.cors_allow_credentials and "*" in self.cors_allow_origins_list:
            raise ValueError(
                "APP_CORS_ALLOW_ORIGINS cannot contain '*' when credentials are enabled."
            )

        if len(secret_value) < 32:
            raise ValueError("APP_SECRET_KEY must be at least 32 characters long.")

        if (self.default_admin_email is None) != (self.default_admin_password is None):
            raise ValueError(
                "APP_DEFAULT_ADMIN_EMAIL and APP_DEFAULT_ADMIN_PASSWORD must be provided together."
            )

        if admin_password is not None and len(admin_password) < 8:
            raise ValueError("APP_DEFAULT_ADMIN_PASSWORD must be at least 8 characters long.")

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]
