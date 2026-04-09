from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import require_roles
from app.db.models.user import User, UserRole
from app.schemas.user import AdminSummaryResponse

router = APIRouter()
RequireAdmin = require_roles(UserRole.ADMIN)
AdminUserDependency = Annotated[User, Depends(RequireAdmin)]


@router.get(
    "/overview",
    response_model=AdminSummaryResponse,
    summary="Get the admin overview",
    description=(
        "Return an admin-only overview response to demonstrate "
        "role-based access control."
    ),
)
async def read_admin_summary(current_user: AdminUserDependency) -> AdminSummaryResponse:
    return AdminSummaryResponse(
        message="Admin access granted.",
        current_user_email=current_user.email,
        current_user_role=current_user.role,
    )
