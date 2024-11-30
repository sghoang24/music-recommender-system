# pylint: disable=E0401
"""User route."""

from typing import List
from uuid import UUID

from api.database.models import db_session
from api.errors.error_message import BaseErrorMessage, EmailRegisteredError, UserNotFoundError
from api.helpers.utils import get_password_hash
from api.responses.base import BaseResponse
from api.schemas.user import UserCreateSchema, UserSchema
from api.services.authentication_service import authentication_service
from api.services.user_service import user_service
from fastapi import APIRouter, Body, Depends
from logger.logger import custom_logger
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", response_model=UserSchema, include_in_schema=True)
async def create_user_account(user: UserCreateSchema, db: Session = Depends(db_session)):
    """Create a new user account."""
    try:
        if user_service.get_user_by_email(db, email=user.email):
            raise ValueError(EmailRegisteredError)

        user = user_service.create_user(db=db, user=user)
        return user

    except ValueError as e:
        error_object: BaseErrorMessage = e.args[0]
        return BaseResponse.error_response(
            message_code=error_object.message_code,
            message=error_object.message,
            status_code=error_object.status_code,
        )
    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message=f"An error occurred: {e}")


@router.post("/preferences", response_model=UserSchema, include_in_schema=True)
async def create_user_preferences(
    preferences: List[str] = Body(..., embed=True),
    db: Session = Depends(db_session),
    current_user: UserSchema = Depends(authentication_service.get_current_user),
):
    """Create user preferences."""
    try:
        if not user_service.get_user_by_id(db=db, user_id=current_user.id):
            raise ValueError(UserNotFoundError)

        return user_service.create_user_preferences(
            db=db,
            user_id=current_user.id,
            preferences=preferences,
        )

    except ValueError as e:
        error_object: BaseErrorMessage = e.args[0]
        return BaseResponse.error_response(
            message_code=error_object.message_code,
            message=error_object.message,
            status_code=error_object.status_code,
        )
    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message=f"An error occurred: {e}")


@router.get("", include_in_schema=True)
async def get_all_users(offset: int = 0, limit: int = 100, db: Session = Depends(db_session)):
    """Get information about all users."""
    try:
        return user_service.get_all_users(db=db, offset=offset, limit=limit)

    except ValueError as e:
        custom_logger.debug(str(e))
        error_object: BaseErrorMessage = e.args[0]
        return BaseResponse.error_response(
            message_code=error_object.message_code,
            message=error_object.message,
            status_code=error_object.status_code,
        )
    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message=f"An error occurred: {e}")


@router.get("/{user_id}", include_in_schema=True)
async def get_user_by_id(user_id: UUID, db: Session = Depends(db_session)):
    """Get information about a user by user ID."""
    try:
        db_user = user_service.get_user_by_id(db=db, user_id=user_id)
        if not db_user:
            raise ValueError(UserNotFoundError)
        return db_user

    except ValueError as e:
        custom_logger.debug(str(e))
        error_object: BaseErrorMessage = e.args[0]
        return BaseResponse.error_response(
            message_code=error_object.message_code,
            message=error_object.message,
            status_code=error_object.status_code,
        )
    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message=f"An error occurred: {e}")


@router.put("/forgot-password/change-password", response_model=UserSchema, include_in_schema=True)
async def change_password_after_reset(email: str, password: str, db: Session = Depends(db_session)):
    """Change the user's password after a successful reset."""
    try:
        if "@" not in email:
            raise ValueError("Email is invalid.")
        password_hash = get_password_hash(password)
        user = user_service.change_password(db, email, password_hash)
        return user

    except ValueError as e:
        error_object: BaseErrorMessage = e.args[0]
        return BaseResponse.error_response(
            message_code=error_object.message_code, message=error_object.message, status_code=error_object.status_code
        )
    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message=f"An error occurred: {e}")


@router.put("/password", response_model=UserSchema, include_in_schema=True)
async def change_password_with_authentication(
    password: str,
    db: Session = Depends(db_session),
    current_user: UserSchema = Depends(authentication_service.get_current_user),
):
    """Change the user's password with authentication."""
    try:
        password_hash = get_password_hash(password)
        user = user_service.change_password(db, current_user.email, password_hash)
        return user

    except ValueError as e:
        error_object: BaseErrorMessage = e.args[0]
        return BaseResponse.error_response(
            message_code=error_object.message_code, message=error_object.message, status_code=error_object.status_code
        )
    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message=f"An error occurred: {e}")
