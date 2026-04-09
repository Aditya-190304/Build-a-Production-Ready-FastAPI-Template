from functools import lru_cache

from pydantic import EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    app_name: str = Field(default="FastAPI Template", validation_alias="APP_NAME")
    app_env: str = Field(default="local", validation_alias="APP_ENV")
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")
    api_v1_prefix: str = Field(default="/api/v1", validation_alias="APP_API_V1_PREFIX")
    version: str = Field(default="0.1.0", validation_alias="APP_VERSION")
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_template",
        validation_alias="APP_DATABASE_URL",
    )
    db_pool_size: int = Field(default=10, validation_alias="APP_DB_POOL_SIZE")
    db_max_overflow: int = Field(default=20, validation_alias="APP_DB_MAX_OVERFLOW")
    db_pool_timeout: int = Field(default=30, validation_alias="APP_DB_POOL_TIMEOUT")
    db_pool_recycle: int = Field(default=1800, validation_alias="APP_DB_POOL_RECYCLE")
    secret_key: SecretStr = Field(
        default=SecretStr("change-me-with-a-long-random-secret"),
        validation_alias="APP_SECRET_KEY",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        validation_alias="APP_ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    default_admin_email: EmailStr = Field(
        default="aditi.admin@example.com",
        validation_alias="APP_DEFAULT_ADMIN_EMAIL",
    )
    default_admin_password: SecretStr = Field(
        default=SecretStr("ChangeMe123!"),
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


@lru_cache
def get_settings() -> Settings:
    return Settings()
