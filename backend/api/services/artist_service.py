# pylint: disable=E0401
"""Artist service."""

from datetime import datetime
from typing import List
from uuid import UUID

from api.database.execute.artist import artist_execute
from api.database.models import Artist
from api.schemas.artist import ArtistCreateSchema, ArtistUpdateSchema
from sqlalchemy.orm import Session


class ArtistService:
    """Artist service."""

    def __init__(self):
        pass

    @staticmethod
    def create_artist(db: Session, artist_schema: ArtistCreateSchema) -> Artist:
        """Create new artist."""
        new_artist = Artist(
            name=artist_schema.name,
            nationality=artist_schema.nationality,
            birthday=artist_schema.birthday,
        )
        return artist_execute.create_artist(db, artist=new_artist)

    @staticmethod
    def create_artists_bulk(db: Session, artist_schemas: List[ArtistCreateSchema]) -> List[Artist]:
        """Bulk create artists."""
        new_artists = [
            Artist(
                name=artist_schema.name,
                nationality=artist_schema.nationality,
                birthday=artist_schema.birthday,
            )
            for artist_schema in artist_schemas
        ]
        return artist_execute.create_artists_bulk(db, new_artists)

    @staticmethod
    def get_artist(db: Session, artist_id: UUID) -> Artist:
        """Get artist."""
        return artist_execute.get_artist(db, artist_id)

    @staticmethod
    def get_artist_by_name(db: Session, artist_name: str) -> List[Artist]:
        """Get artist by name."""
        return artist_execute.get_artist_by_name(db, artist_name)

    @staticmethod
    def search_artists_by_name(db: Session, artist_name: str) -> List[Artist]:
        """Search artists by name."""
        return artist_execute.search_artists_by_name(db, artist_name)

    @staticmethod
    def get_all_artists(db: Session, offset: int = 0, limit: int = 100) -> List[Artist]:
        """Get all artist."""
        return artist_execute.get_all_artists(db, offset, limit)

    @staticmethod
    def update_artist(db: Session, update_info: dict) -> Artist:
        """Update artist."""
        birthday = update_info.get("birthday", None)
        if isinstance(birthday, str):
            birthday = datetime.strptime(birthday, "%Y-%m-%d")
        update_info = ArtistUpdateSchema(
            id=update_info.get("id", None),
            name=update_info.get("name", None),
            nationality=update_info.get("nationality", None),
            birthday=birthday,
        )
        return artist_execute.update_artist(db, update_info)

    @staticmethod
    def delete_artist(db: Session, artist_id: UUID) -> Artist:
        """Delete artist."""
        return artist_execute.delete_artist(db, artist_id)


artist_service = ArtistService()
