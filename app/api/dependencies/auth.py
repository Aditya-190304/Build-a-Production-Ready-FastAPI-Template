from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    AuthenticationRequiredError,
    AuthorizationError,
    InvalidTokenError,
    UserUnavailableError,
)
from app.core.security import InvalidTokenError as JwtInvalidTokenError
from app.core.security import decode_access_token
from app.db.models.user import User, UserRole
from app.db.session import get_db
from app.services.users import get_user_by_email

bearer_scheme = HTTPBearer(
    auto_error=False,
    description="Paste the JWT access token returned by the login endpoint.",
)
CredentialsDependency = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]
DatabaseDependency = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    credentials: CredentialsDependency,
    db: DatabaseDependency,
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationRequiredError()

    try:
        payload = decode_access_token(credentials.credentials)
    except JwtInvalidTokenError as exc:
        raise InvalidTokenError() from exc

    email = payload.get("sub")
    if not isinstance(email, str):
        raise InvalidTokenError(message="Invalid token payload.")

    user = await get_user_by_email(db, email)
    if user is None or not user.is_active:
        raise UserUnavailableError()

    return user


def require_roles(*allowed_roles: UserRole) -> Callable[[User], User]:
    current_user_dependency = Depends(get_current_user)

    async def dependency(current_user: Annotated[User, current_user_dependency]) -> User:
        if current_user.role not in allowed_roles:
            raise AuthorizationError()
        return current_user

    return dependency
