# pylint: disable=E0401
"""Album service."""

from typing import List
from uuid import UUID

from api.database.execute.album import album_execute
from api.database.models import Album
from api.schemas.album import AlbumCreateSchema, AlbumUpdateSchema
from sqlalchemy.orm import Session


class AlbumService:
    """Album service."""

    def __init__(self):
        pass

    @staticmethod
    def create_album(db: Session, album_schema: AlbumCreateSchema) -> Album:
        """Create new album."""
        new_album = Album(name=album_schema.name, release_date=album_schema.release_date)
        return album_execute.create_album(db, album=new_album)

    @staticmethod
    def create_albums_bulk(db: Session, album_schemas: List[AlbumCreateSchema]) -> List[Album]:
        """Bulk create albums."""
        new_albums = [
            Album(
                name=album_schema.name,
                release_date=album_schema.release_date,
            )
            for album_schema in album_schemas
        ]
        return album_execute.create_albums_bulk(db, new_albums)

    @staticmethod
    def get_album(db: Session, album_id: UUID) -> Album:
        """Get album."""
        return album_execute.get_album(db, album_id)

    @staticmethod
    def get_album_by_name(db: Session, album_name: str) -> List[Album]:
        """Get album by name."""
        return album_execute.get_album_by_name(db, album_name)

    @staticmethod
    def search_albums_by_name(db: Session, album_name: str) -> List[Album]:
        """Search albums by name."""
        return album_execute.search_albums_by_name(db, album_name)

    @staticmethod
    def get_all_albums(db: Session, offset: int = 0, limit: int = 100) -> List[Album]:
        """Get all album."""
        return album_execute.get_all_albums(db, offset, limit)

    @staticmethod
    def update_album(db: Session, update_info: dict) -> Album:
        """Update album."""
        update_info = AlbumUpdateSchema(
            id=update_info.get("id", None),
            name=update_info.get("name", None),
            release_date=update_info.get("release_date", None),
        )
        return album_execute.update_album(db, update_info)

    @staticmethod
    def delete_album(db: Session, album_id: UUID) -> Album:
        """Delete album."""
        return album_execute.delete_album(db, album_id)


album_service = AlbumService()
