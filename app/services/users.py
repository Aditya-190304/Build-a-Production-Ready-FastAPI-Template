from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password, verify_password
from app.db.models.user import User, UserRole


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email.lower())
    return db.scalar(statement)


def create_user(db: Session, *, email: str, password: str, role: UserRole = UserRole.USER) -> User:
    user = User(
        email=email.lower(),
        hashed_password=hash_password(password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, *, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


def seed_default_admin(db: Session) -> None:
    settings = get_settings()
    if get_user_by_email(db, settings.default_admin_email) is not None:
        return
    create_user(
        db,
        email=settings.default_admin_email,
        password=settings.default_admin_password.get_secret_value(),
        role=UserRole.ADMIN,
    )
