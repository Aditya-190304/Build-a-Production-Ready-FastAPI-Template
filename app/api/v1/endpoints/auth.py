from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.auth import TokenResponse, UserLoginRequest, UserRegisterRequest
from app.schemas.user import UserResponse
from app.services.users import authenticate_user, create_user, get_user_by_email

router = APIRouter()
DatabaseDependency = Annotated[Session, Depends(get_db)]


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a standard user account using an email address and password.",
    responses={
        201: {"description": "User registered successfully."},
        409: {"description": "A user with this email already exists."},
    },
)
def register_user(payload: UserRegisterRequest, db: DatabaseDependency) -> UserResponse:
    if get_user_by_email(db, payload.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = create_user(db, email=payload.email, password=payload.password)
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and obtain a JWT",
    description=(
        "Authenticate with email and password and receive a bearer token "
        "for protected routes."
    ),
    responses={
        200: {"description": "Authentication successful."},
        401: {"description": "Invalid email or password."},
    },
)
def login_user(payload: UserLoginRequest, db: DatabaseDependency) -> TokenResponse:
    user = authenticate_user(db, email=payload.email, password=payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(subject=user.email, role=user.role)
    return TokenResponse(access_token=access_token)
