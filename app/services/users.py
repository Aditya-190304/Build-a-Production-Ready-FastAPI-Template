from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.constants import DEFAULT_ADMIN_FULL_NAME
from app.core.security import hash_password, verify_password
from app.db.models.user import User, UserRole


class UserAlreadyExistsError(Exception):
    pass


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email.lower())
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    *,
    email: str,
    password: str,
    full_name: str,
    role: UserRole = UserRole.USER,
) -> User:
    user = User(
        email=email.lower(),
        full_name=full_name,
        password_hash=hash_password(password),
        role=role,
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise UserAlreadyExistsError("A user with this email already exists.") from exc
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, *, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user


async def seed_default_admin(db: AsyncSession) -> None:
    settings = get_settings()
    if settings.default_admin_email is None or settings.default_admin_password is None:
        raise RuntimeError(
            "APP_DEFAULT_ADMIN_EMAIL and APP_DEFAULT_ADMIN_PASSWORD are required to seed the admin."
        )
    if await get_user_by_email(db, settings.default_admin_email) is not None:
        return
    await create_user(
        db,
        email=settings.default_admin_email,
        password=settings.default_admin_password.get_secret_value(),
        full_name=DEFAULT_ADMIN_FULL_NAME,
        role=UserRole.ADMIN,
    )
