# pylint: disable=E0401
"""Authentication route."""

import base64
from datetime import timedelta

from api.database.models import db_session
from api.errors.error_message import BaseErrorMessage, IncorrectEmailOrPassword
from api.responses.base import BaseResponse, HttpResponseSchema
from api.schemas.auth import BasicAuth, basic_auth
from api.schemas.token import TokenSchema
from api.schemas.user import UserSchema
from api.services.authentication_service import authentication_service
from api.services.user_service import user_service
from core.constant import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from logger.logger import custom_logger
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, Response

router = APIRouter()


@router.post("/token", response_model=TokenSchema, include_in_schema=True)
async def login_to_obtain_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db_session),
):
    """Login to obtain an access token."""
    try:
        user = authentication_service.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise ValueError(IncorrectEmailOrPassword)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = authentication_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        response = BaseResponse.success_response(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user.id,
                "role": user.role,
                "preferences": user_service.check_user_preferences(db, user.id),
            }
        )
        response.set_cookie(
            "Authorization",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return response

    except ValueError as e:
        custom_logger.debug(str(e))
        error_object: BaseErrorMessage = e.args[0]
        return BaseResponse.error_response(
            message_code=error_object.message_code, message=error_object.message, status_code=error_object.status_code
        )
    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message=f"An error occurred: {e}")


@router.get("/logout", response_model=HttpResponseSchema)
async def logout_and_remove_cookie():
    """Logout and remove the Authorization cookie."""
    response = BaseResponse.success_response()
    response.delete_cookie("Authorization")
    return response


@router.get("/docs/logout")
async def logout_docs_and_remove_cookie():
    """Logout from documentation and remove the Authorization cookie."""
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization")
    return response


@router.get("/docs/login", include_in_schema=False)
async def login_to_swagger_docs(auth: BasicAuth = Depends(basic_auth), db: Session = Depends(db_session)):
    """Login to Swagger docs and obtain an access token."""
    if not auth:
        return Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)

    try:
        decoded = base64.b64decode(auth).decode("ascii")
        email, _, password = decoded.partition(":")
        user = authentication_service.authenticate_user(db, email, password, True)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = authentication_service.create_access_token(
            data={"sub": email}, expires_delta=access_token_expires
        )

        token = jsonable_encoder(access_token)

        response = RedirectResponse(url="/docs")
        response.set_cookie(
            "Authorization",
            value=f"Bearer {token}",
            httponly=True,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return response

    except HTTPException:
        return Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message=f"An error occurred: {e}")


@router.get("/user/me", response_model=UserSchema)
async def get_current_information(
    current_user: UserSchema = Depends(authentication_service.get_current_user)
):
    """Get information of the current user."""
    return current_user
