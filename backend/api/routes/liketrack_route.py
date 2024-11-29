# pylint: disable=E0401
"""Liked Track routes."""

from typing import List

from api.database.models import db_session
from api.errors.error_message import BaseErrorMessage
from api.responses.base import BaseResponse
from api.schemas.liked_track import LikedTrackCreateSchema
from api.services.liketrack_service import liketrack_service
from fastapi import APIRouter, Depends
from logger.logger import custom_logger
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", include_in_schema=True)
async def create_liked_track(like_track_schema: LikedTrackCreateSchema, db: Session = Depends(db_session)):
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


@router.post("/bulk", include_in_schema=True)
async def create_liked_tracks_bulk(like_track_schemas: List[LikedTrackCreateSchema], db: Session = Depends(db_session)):
    """Bulk create liked tracks."""
    try:
        return liketrack_service.create_liked_tracks_bulk(db, like_track_schemas)
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
