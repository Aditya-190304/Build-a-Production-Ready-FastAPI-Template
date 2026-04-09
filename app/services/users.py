from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import hash_password, verify_password
from app.db.models.user import User, UserRole


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
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, *, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user


async def seed_default_admin(db: AsyncSession) -> None:
    settings = get_settings()
    if await get_user_by_email(db, settings.default_admin_email) is not None:
        return
    await create_user(
        db,
        email=settings.default_admin_email,
        password=settings.default_admin_password.get_secret_value(),
        full_name="Aditi Sharma",
        role=UserRole.ADMIN,
    )
