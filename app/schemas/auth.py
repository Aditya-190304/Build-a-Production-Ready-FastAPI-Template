from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.constants import EXAMPLE_STRONG_PASSWORD, EXAMPLE_USER_EMAIL, EXAMPLE_USER_FULL_NAME


class UserRegisterRequest(BaseModel):
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Display name for the user account.",
        examples=[EXAMPLE_USER_FULL_NAME],
    )
    email: EmailStr = Field(
        ...,
        description="Unique email address used to sign in.",
        examples=[EXAMPLE_USER_EMAIL],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Plain-text password that will be securely hashed before storage.",
        examples=[EXAMPLE_STRONG_PASSWORD],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": EXAMPLE_USER_FULL_NAME,
                "email": EXAMPLE_USER_EMAIL,
                "password": EXAMPLE_STRONG_PASSWORD,
            }
        }
    )

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if not normalized:
            raise ValueError("Full name must not be blank.")
        return normalized

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        checks = {
            "uppercase": any(character.isupper() for character in value),
            "lowercase": any(character.islower() for character in value),
            "digit": any(character.isdigit() for character in value),
            "special": any(not character.isalnum() for character in value),
        }
        if not all(checks.values()):
            raise ValueError(
                "Password must include at least one uppercase letter, one lowercase letter, "
                "one number, and one special character."
            )
        return value


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Registered email address.",
        examples=[EXAMPLE_USER_EMAIL],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Account password.",
        examples=[EXAMPLE_STRONG_PASSWORD],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": EXAMPLE_USER_EMAIL,
                "password": EXAMPLE_STRONG_PASSWORD,
            }
        }
    )


class TokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="JWT access token to include in the Authorization header as `Bearer <token>`.",
    )
    token_type: str = Field(default="bearer", examples=["bearer"])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example",
                "token_type": "bearer",
            }
        }
    )
