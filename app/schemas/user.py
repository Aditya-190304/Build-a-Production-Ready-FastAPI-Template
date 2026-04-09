from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.db.models.user import UserRole


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "full_name": "Priya Sharma",
                "email": "priya.sharma@example.com",
                "role": "user",
                "is_active": True,
                "created_at": "2026-01-01T12:00:00Z",
                "updated_at": "2026-01-01T12:00:00Z",
            }
        },
    )


class AdminSummaryResponse(BaseModel):
    message: str = Field(examples=["Admin access granted."])
    current_user_email: EmailStr
    current_user_role: UserRole

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Admin access granted.",
                "current_user_email": "aditi.admin@example.com",
                "current_user_role": "admin",
            }
        }
    )
