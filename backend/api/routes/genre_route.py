"""Genre route."""

from uuid import UUID
from typing import List

from api.database.models import db_session
from api.errors.error_message import BaseErrorMessage
from api.responses.base import BaseResponse
from api.schemas.genre import GenreCreateSchema, GenreUpdateSchema
from api.services.genre_service import genre_service
from fastapi import APIRouter, Depends
from logger.logger import custom_logger
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", include_in_schema=True)
async def create_genre(genre_schema: GenreCreateSchema, db: Session = Depends(db_session)):
    """Create genre."""
    try:
        return genre_service.create_genre(db, genre_schema)

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
async def create_genres_bulk(genre_schemas: List[GenreCreateSchema], db: Session = Depends(db_session)):
    """Bulk create genres."""
    try:
        return genre_service.create_genres_bulk(db, genre_schemas)

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
async def get_genre(genre_id: UUID, db: Session = Depends(db_session)):
    """Get genre."""
    try:
        return genre_service.get_genre(db, genre_id)

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
async def get_all_genres(offset: int = 0, limit: int = 10, db: Session = Depends(db_session)):
    """Get all genres."""
    try:
        return genre_service.get_all_genres(db, offset, limit)

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
async def update_genre(genre_schema: GenreUpdateSchema, db: Session = Depends(db_session)):
    """Update genre."""
    try:
        return genre_service.update_genre(db, genre_schema.dict())

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
async def delete_genre(genre_id: UUID, db: Session = Depends(db_session)):
    """Delete genre."""
    try:
        return genre_service.delete_genre(db, genre_id)

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
async def search_genres_by_name(genre_name: str, db: Session = Depends(db_session)):
    """Search genres by name.""" 
    try:
        genres = genre_service.search_genres_by_name(db, genre_name)
        return BaseResponse.success_response(data=genres)
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
async def get_genre_by_name(genre_name: str, db: Session = Depends(db_session)):
    """Get genre by exact name."""
    try:
        genre = genre_service.get_genre_by_name(db, genre_name)
        return BaseResponse.success_response(data=genre)
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
