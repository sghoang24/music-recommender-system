# pylint: disable=E0401
"""User Service."""

from typing import List, Type
from uuid import UUID

from api.database.execute import user as user_execute
from api.database.models import User
from api.helpers.utils import get_password_hash
from api.schemas.user import UserCreateSchema
from logger.logger import custom_logger
from ratelimit import limits
from sqlalchemy.orm import Session


class UserService:
    """User Service."""

    def __init__(self):
        pass

    def create_user(self, db: Session, user: UserCreateSchema) -> User:
        """Add user to database."""
        # Create user
        user.password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=user.password,
            full_name=user.full_name,
            role=1 if user.email == "hoangnguyennho24@gmail.com" else 0,  # 0 for user / 1 for admin
        )
        user_execute.create_user(db, db_user)

        return db_user

    @staticmethod
    def change_password(db: Session, email: str, password: str):
        """Change password."""
        return user_execute.change_password(db, email, password)

    @staticmethod
    def delete_user(db: Session, user_id: UUID):
        """Delete user."""
        return user_execute.delete_user(db, user_id)

    @staticmethod
    @limits(calls=1, period=60)
    def limited_endpoint(input_data: str):
        """Limited endpoint."""
        return f"You've accessed this with input: {input_data}"

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> Type[User] | None:
        """Get user."""
        return user_execute.get_user(db, user_id)

    @staticmethod
    def get_all_users(db: Session, offset: int = 0, limit: int = 100) -> List[User]:
        """Get all user."""
        return user_execute.get_all_users(db, offset, limit)

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email."""
        return user_execute.get_user_by_email(db, email)

    @staticmethod
    def create_user_admin(db: Session):
        """Create user admin."""
        admin_email = "hoangnguyennho24@gmail.com"
        if not user_execute.get_user_by_email(db, admin_email):
            custom_logger.info("Creating admin user...")
            hash_password = get_password_hash("24092002")
            db_user = User(email=admin_email, hashed_password=hash_password, full_name="Nguyen Nho Song Hoang", role=1)
            user_execute.create_user(db, db_user)
            return db_user
        return None

    @staticmethod
    def create_user_preferences(db: Session, user_id: UUID, preferences: List[str]):
        """Create user preferences."""
        return user_execute.create_user_preferences(db, user_id, preferences)

    @staticmethod
    def check_user_preferences(db: Session, user_id: UUID):
        """Check user preferences."""
        return user_execute.check_user_preferences(db, user_id)


user_service = UserService()
