# pylint: disable=E0401
"""Track route."""


# )
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from api.errors.error_message import BaseErrorMessage
from api.responses.base import BaseResponse
from api.services.track_service import track_service
from api.database.models import db_session
from api.schemas.track import TrackCreateSchema, TrackUpdateSchema
from sqlalchemy.orm import Session
from logger.logger import custom_logger
# from api.services.artist_service import artist_service

# from api.schemas.artist import (


router = APIRouter()

@router.get("/get-all", include_in_schema=True)
async def get_all_tracks(offset: int = 0, limit: int = 10, db: Session = Depends(db_session)):
    """Get all tracks."""
    try : 
        return track_service.get_all_tracks(db=db, offset=offset, limit=limit)
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

@router.get("/get-by-id", include_in_schema=True)
async def get_track_by_id(track_id: UUID, db: Session = Depends(db_session)):
    """Get track by id."""
    try:
        return track_service.get_track(db, track_id)
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
        
@router.post("", include_in_schema=True)
async def create_track(track_schema: TrackCreateSchema, db: Session = Depends(db_session)):
    """Create track."""
    try:
        return track_service.create_track(db, track_schema)
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
async def create_tracks_bulk(track_schemas: List[TrackCreateSchema], db: Session = Depends(db_session)):
    """Bulk create tracks."""
    try:
        return track_service.create_tracks_bulk(db, track_schemas)
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
        
@router.put("", include_in_schema=True)
async def update_track(track_update: TrackUpdateSchema, db: Session = Depends(db_session)):
    """Update track."""
    try:
        updated_track = track_service.update_track(db, track_update)
        return BaseResponse.success_response(data=updated_track)
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
        
@router.delete("", include_in_schema=True)
async def delete_track(track_id: UUID, db: Session = Depends(db_session)):
    """Delete track."""
    try:
        return track_service.delete_track(db, track_id)
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
    
@router.get("/get-by-name", include_in_schema=True)
async def get_track_by_name(track_name: str, db: Session = Depends(db_session)):
    """Get track by exact name."""
    try:
        return track_service.get_track_by_name(db, track_name)
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
    
@router.get("/search", include_in_schema=True)
async def search_tracks(search_query : str, genres: str = "all", db: Session = Depends(db_session)):
    """Search tracks by name."""
    try:
        return track_service.search_tracks(db=db, search_query=search_query, genres=genres)
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
    
