from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.db.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()
CurrentUserDependency = Annotated[User, Depends(get_current_user)]


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get the current authenticated user",
    description="Return the currently authenticated user profile for the supplied bearer token.",
)
def read_current_user(current_user: CurrentUserDependency) -> UserResponse:
    return UserResponse.model_validate(current_user)
