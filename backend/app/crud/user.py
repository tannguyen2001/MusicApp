"""
User CRUD operations
"""

import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    """Create new user"""
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user(*, session: Session, user_id: uuid.UUID) -> User | None:
    """Get user by ID"""
    return session.get(User, user_id)


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """Get user by email"""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_users(*, session: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get list of users"""
    statement = select(User).offset(skip).limit(limit)
    return list(session.exec(statement))


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> User:
    """Update user"""
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(*, session: Session, user_id: uuid.UUID) -> bool:
    """Delete user"""
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    """Authenticate user"""
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
