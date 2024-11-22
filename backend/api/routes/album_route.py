# pylint: disable=E0401
"""Album route."""

from uuid import UUID

from api.database.models import db_session
from api.errors.error_message import BaseErrorMessage
from api.responses.base import BaseResponse
from api.schemas.album import AlbumCreateSchema, AlbumUpdateSchema
from api.services.album_service import album_service
from fastapi import APIRouter, Depends
from logger.logger import custom_logger
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", include_in_schema=True)
async def create_album(album_schema: AlbumCreateSchema, db: Session = Depends(db_session)):
    """Create a new album."""
    try:
        return album_service.create_album(db, album_schema)

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
async def get_album(album_id: UUID, db: Session = Depends(db_session)):
    """Get album."""
    try:
        return album_service.get_album(db, album_id)

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
async def get_album_by_name(album_name: str, db: Session = Depends(db_session)):
    """Get album by name."""
    try:
        return album_service.get_album_by_name(db, album_name)

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
async def search_albums_by_name(album_name: str, db: Session = Depends(db_session)):
    """Search albums by name."""
    try:
        return album_service.search_albums_by_name(db, album_name)

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
async def get_all_albums(offset: int = 0, limit: int = 10, db: Session = Depends(db_session)):
    """Get all albums."""
    try:
        return album_service.get_all_albums(db, offset, limit)

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
async def update_album(album_schema: AlbumUpdateSchema, db: Session = Depends(db_session)):
    """Update album."""
    try:
        return album_service.update_album(db, album_schema.dict())

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
async def delete_album(album_id: UUID, db: Session = Depends(db_session)):
    """Delete album."""
    try:
        return album_service.delete_album(db, album_id)

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
