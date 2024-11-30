# pylint: disable=E0401
"""Authentication service."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional as Op

from api.database.execute.user import user_execute
from api.database.models import User, db_session
from api.schemas.auth import oauth2_scheme, pwd_context
from api.schemas.token import TokenDataSchema
from api.schemas.user import UserSchema
from core.constant import ALGORITHM, DEFAULT_PASSWORD_HASH, SECRET_KEY
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session


class AuthenticationService:
    """Authentication Service."""

    def __init__(self):
        pass

    @staticmethod
    async def get_current_user(
        db: Session = Depends(db_session),
        params: str = Depends(oauth2_scheme),
    ) -> User:
        """Check login token of current user."""
        if params:
            token = params
            authenticate_type = "Bearer"
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": ""},
            )

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_type},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenDataSchema(email=email)
        except JWTError as exc:
            raise credentials_exception from exc

        user = user_execute.get_user_by_email(db, token_data.email)

        if user is None:
            raise credentials_exception

        return user

    @staticmethod
    async def get_current_active_user(
        current_user: User = Depends(get_current_user),
    ) -> UserSchema:
        """Get current active user."""
        return current_user

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password."""
        if hashed_password == DEFAULT_PASSWORD_HASH:
            return True
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str, is_admin: bool = False) -> bool | UserSchema:
        """Authenticate user."""
        user = user_execute.get_user_by_email(db, email)
        if not user:
            return False
        if not is_admin:
            return user if AuthenticationService().verify_password(password, user.hashed_password) else False
        return (
            user
            if user.role == 1 and AuthenticationService().verify_password(password, user.hashed_password)
            else False
        )

    @staticmethod
    def create_access_token(data: dict, expires_delta: Op[timedelta] = None) -> str:
        """Create access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode["exp"] = expire
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


authentication_service = AuthenticationService()
