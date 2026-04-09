from datetime import UTC, datetime, timedelta

import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import get_settings
from app.core.constants import JWT_ALGORITHM
from app.db.models.user import UserRole

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(*, subject: str, role: UserRole, expires_minutes: int | None = None) -> str:
    settings = get_settings()
    lifetime_minutes = expires_minutes or settings.access_token_expire_minutes
    expires_at = datetime.now(UTC) + timedelta(minutes=lifetime_minutes)
    payload = {
        "sub": subject,
        "role": role.value,
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.secret_key.get_secret_value(), algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, str]:
    settings = get_settings()
    payload = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=[JWT_ALGORITHM])
    return payload


__all__ = [
    "InvalidTokenError",
    "create_access_token",
    "decode_access_token",
    "hash_password",
    "verify_password",
]
