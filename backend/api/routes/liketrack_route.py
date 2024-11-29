# pylint: disable=E0401
"""Liked Track routes."""

from typing import List

from api.database.models import db_session
from api.errors.error_message import BaseErrorMessage
from api.responses.base import BaseResponse
from api.schemas.liked_track import (
    LikedTrackCreateSchema,
    LikedTrackGetSchema,
)
from api.services.liketrack_service import liketrack_service
from fastapi import APIRouter, Depends
from logger.logger import custom_logger
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/liked", include_in_schema=True)
async def create_liked_track(
    like_track_schema: LikedTrackCreateSchema,
    db: Session = Depends(db_session)
):
    """Create a new liked track."""
    try:
        return liketrack_service.create_liked_track(db, like_track_schema)
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


@router.post("/bulk-liked", include_in_schema=True)
async def create_liked_tracks_bulk(
    liked_track_schemas: List[LikedTrackCreateSchema],
    db: Session = Depends(db_session)
):
    """Bulk create liked tracks."""
    try:
        return liketrack_service.create_liked_tracks_bulk(db, liked_track_schemas)
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


@router.post("/check-liked", include_in_schema=True)
async def check_liked_track(
    liked_track_schema: LikedTrackCreateSchema,
    db: Session = Depends(db_session)
):
    """Check liked track."""
    try:
        if liketrack_service.get_liked_track(db, liked_track_schema):
            return {"is_liked": True}
        return {"is_liked": False}

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


@router.post("/unliked", include_in_schema=True)
async def unliked_track(
    liked_track_schema: LikedTrackCreateSchema,
    db: Session = Depends(db_session)
):
    """Check liked track."""
    try:
        return liketrack_service.get_liked_track(db, liked_track_schema)

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


@router.post("/get-by-user", include_in_schema=True)
async def get_liked_tracks_by_user(
    liked_track_schema: LikedTrackGetSchema,
    db: Session = Depends(db_session)
):
    """Get liked tracks by user."""
    try:
        return liketrack_service.get_liked_tracks_by_user(db, liked_track_schema)

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
