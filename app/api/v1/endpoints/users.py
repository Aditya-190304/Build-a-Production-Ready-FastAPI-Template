from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.auth import UserRegisterRequest
from app.schemas.user import UserResponse
from app.services.users import create_user, get_user_by_email

router = APIRouter()
CurrentUserDependency = Annotated[User, Depends(get_current_user)]
DatabaseDependency = Annotated[AsyncSession, Depends(get_db)]


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user account",
    description=(
        "Create a standard user account with a full name, unique email address, "
        "and password."
    ),
    responses={
        201: {"description": "User account created successfully."},
        409: {"description": "A user with this email already exists."},
    },
)
async def create_user_account(
    payload: UserRegisterRequest,
    db: DatabaseDependency,
) -> UserResponse:
    if await get_user_by_email(db, payload.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = await create_user(
        db,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )
    return UserResponse.model_validate(user)


@router.get(
    "/current",
    response_model=UserResponse,
    summary="Get the current authenticated user",
    description=(
        "Return the user profile associated with the supplied bearer token."
    ),
)
async def read_current_user(current_user: CurrentUserDependency) -> UserResponse:
    return UserResponse.model_validate(current_user)
