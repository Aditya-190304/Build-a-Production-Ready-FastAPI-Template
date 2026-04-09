from functools import lru_cache

from pydantic import EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="FastAPI Template", validation_alias="APP_NAME")
    app_env: str = Field(default="local", validation_alias="APP_ENV")
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")
    api_v1_prefix: str = Field(default="/api/v1", validation_alias="APP_API_V1_PREFIX")
    version: str = Field(default="0.1.0", validation_alias="APP_VERSION")
    database_url: str = Field(
        default="sqlite:///./fastapi_template.db",
        validation_alias="APP_DATABASE_URL",
    )
    secret_key: SecretStr = Field(
        default=SecretStr("change-me-with-a-long-random-secret"),
        validation_alias="APP_SECRET_KEY",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        validation_alias="APP_ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    default_admin_email: EmailStr = Field(
        default="admin@example.com",
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


@lru_cache
def get_settings() -> Settings:
    return Settings()
