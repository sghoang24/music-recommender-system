# pylint: disable=E0401
"""Artist route."""

from uuid import UUID
from typing import List

from api.database.models import db_session
from api.errors.error_message import BaseErrorMessage
from api.responses.base import BaseResponse
from api.schemas.artist import ArtistCreateSchema, ArtistUpdateSchema
from api.services.artist_service import artist_service
from fastapi import APIRouter, Depends
from logger.logger import custom_logger
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("", include_in_schema=True)
async def create_artist(artist_schema: ArtistCreateSchema, db: Session = Depends(db_session)):
    """Create artist."""
    try:
        return artist_service.create_artist(db, artist_schema)

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
async def create_artists_bulk(artist_schemas: List[ArtistCreateSchema], db: Session = Depends(db_session)):
    """Bulk create artists."""
    try:
        return artist_service.create_artists_bulk(db, artist_schemas)

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
async def get_artist(artist_id: UUID, db: Session = Depends(db_session)):
    """Get artist."""
    try:
        return artist_service.get_artist(db, artist_id)

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


@router.get("/get-all", include_in_schema=True)
async def get_all_artists(offset: int = 0, limit: int = 10, db: Session = Depends(db_session)):
    """Get all artists."""
    try:
        return artist_service.get_all_artists(db, offset, limit)

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
async def update_artist(artist_schema: ArtistUpdateSchema, db: Session = Depends(db_session)):
    """Update artist."""
    try:
        return artist_service.update_artist(db, artist_schema.dict())

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
async def delete_artist(artist_id: UUID, db: Session = Depends(db_session)):
    """Delete artist."""
    try:
        return artist_service.delete_artist(db, artist_id)

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
async def search_artists_by_name(artist_name: str, db: Session = Depends(db_session)):
    """Search artists by name.""" 
    try:
        artists = artist_service.search_artists_by_name(db, artist_name)
        return BaseResponse.success_response(data=artists)
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


@router.get("/get-by-name",include_in_schema=True)
async def get_artist_by_name(artist_name: str, db: Session = Depends(db_session)):
    """Get artist by exact name."""
    try:
        artist = artist_service.get_artist_by_name(db, artist_name)
        return BaseResponse.success_response(data=artist)
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