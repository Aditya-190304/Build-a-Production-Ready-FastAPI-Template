from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.auth import TokenResponse, UserLoginRequest
from app.services.users import authenticate_user

router = APIRouter()
DatabaseDependency = Annotated[AsyncSession, Depends(get_db)]


@router.post(
    "/tokens",
    response_model=TokenResponse,
    summary="Create an access token",
    description=(
        "Authenticate with an email address and password, then issue "
        "a bearer token for protected routes."
    ),
    responses={
        200: {"description": "Access token issued successfully."},
        401: {"description": "Invalid email or password."},
    },
)
async def login_user(payload: UserLoginRequest, db: DatabaseDependency) -> TokenResponse:
    user = await authenticate_user(db, email=payload.email, password=payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(subject=user.email, role=user.role)
    return TokenResponse(access_token=access_token)
