# pylint: disable=E0401
"""User execute."""

from datetime import datetime
from typing import List, Type
from uuid import UUID

from api.database.models import User
from core.config import GENRES_MAP
from sqlalchemy import orm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: UUID) -> Type[User] | None:
    """Get user."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_ids(db: Session, user_ids: list[UUID]):
    """Get user by list of user id."""
    return db.query(User).filter(User.id.in_(user_ids)).all()


def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session, offset: int = 0, limit: int = 100):
    """Get all users with offset and limit."""
    query = db.query(User)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    query = query.options(orm.undefer(User.updated_at))
    return query.all()


def create_user(db: Session, user: User):
    """Create new user."""
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_active_status(db: Session, email: str, is_active: bool):
    """Confirm activate user."""
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.is_active = is_active
        user.updated_at = datetime.utcnow()
        db.commit()
        return user


def create_user_preferences(db: Session, user_id: UUID, preferences: List[str] = None):
    """Create user preferences."""
    user = db.query(User).filter(User.id == user_id).first()
    preferences = [GENRES_MAP[preference] for preference in preferences]
    user.preferences = preferences
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def check_user_preferences(db: Session, user_id: UUID):
    """Check user preferences."""
    user = db.query(User).filter(User.id == user_id).first()
    return True if user.preferences else False


def change_password(db: Session, email: str, password: str):
    """Confirm activate user."""
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.hashed_password = password
        db.commit()
        return user


def delete_user(db: Session, user_id: UUID):
    """Delete user."""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        return user
    except IntegrityError as e:
        # Handle any IntegrityError, such as foreign key violations here
        db.rollback()
        raise e
