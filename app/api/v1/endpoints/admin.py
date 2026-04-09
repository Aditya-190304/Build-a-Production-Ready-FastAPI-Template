from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import require_roles
from app.db.models.user import User, UserRole
from app.schemas.user import AdminSummaryResponse

router = APIRouter()
RequireAdmin = require_roles(UserRole.ADMIN)
AdminUserDependency = Annotated[User, Depends(RequireAdmin)]


@router.get(
    "/summary",
    response_model=AdminSummaryResponse,
    summary="Admin-only example route",
    description=(
        "Demonstrates role-based access control by restricting this route "
        "to administrators."
    ),
)
def read_admin_summary(current_user: AdminUserDependency) -> AdminSummaryResponse:
    return AdminSummaryResponse(
        message="Admin access granted.",
        current_user_email=current_user.email,
        current_user_role=current_user.role,
    )
