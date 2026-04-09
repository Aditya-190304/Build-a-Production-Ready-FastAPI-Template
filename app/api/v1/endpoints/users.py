from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.api.docs import error_response_doc
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.auth import UserRegisterRequest
from app.schemas.user import UserResponse
from app.services.users import create_user

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
        **error_response_doc(
            status_code=409,
            description="A user with this email already exists.",
            code="conflict",
            message="A user with this email already exists.",
        ),
        **error_response_doc(
            status_code=422,
            description="Request validation failed.",
            code="validation_error",
            message="Request validation failed.",
            details=[
                {
                    "field": "body.password",
                    "message": (
                        "Password must include at least one uppercase letter, one lowercase "
                        "letter, one number, and one special character."
                    ),
                    "type": "value_error",
                }
            ],
        ),
    },
)
async def create_user_account(
    payload: UserRegisterRequest,
    db: DatabaseDependency,
) -> UserResponse:
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
    responses={
        **error_response_doc(
            status_code=401,
            description="Authentication credentials are missing or invalid.",
            code="unauthorized",
            message="Authentication credentials were not provided.",
        )
    },
)
async def read_current_user(current_user: CurrentUserDependency) -> UserResponse:
    return UserResponse.model_validate(current_user)
