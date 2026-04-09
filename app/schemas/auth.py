from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegisterRequest(BaseModel):
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Display name for the user account.",
        examples=["Priya Sharma"],
    )
    email: EmailStr = Field(
        ...,
        description="Unique email address used to sign in.",
        examples=["priya.sharma@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Plain-text password that will be securely hashed before storage.",
        examples=["StrongPassword123!"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "Priya Sharma",
                "email": "priya.sharma@example.com",
                "password": "StrongPassword123!",
            }
        }
    )


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Registered email address.",
        examples=["priya.sharma@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Account password.",
        examples=["StrongPassword123!"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "priya.sharma@example.com",
                "password": "StrongPassword123!",
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
