from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.docs import error_response_doc
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
        **error_response_doc(
            status_code=401,
            description="Invalid email or password.",
            code="unauthorized",
            message="Invalid email or password.",
        ),
        **error_response_doc(
            status_code=422,
            description="Request validation failed.",
            code="validation_error",
            message="Request validation failed.",
            details=[
                {
                    "field": "body.email",
                    "message": "value is not a valid email address",
                    "type": "value_error",
                }
            ],
        ),
    },
)
async def login_user(payload: UserLoginRequest, db: DatabaseDependency) -> TokenResponse:
    user = await authenticate_user(db, email=payload.email, password=payload.password)
    access_token = create_access_token(subject=user.email, role=user.role)
    return TokenResponse(access_token=access_token)
