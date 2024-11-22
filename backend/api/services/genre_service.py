# pylint: disable=E0401
"""Genre service."""

from typing import List
from uuid import UUID

from api.database.execute import genre as genre_execute
from api.database.models import Genre
from api.schemas.genre import GenreCreateSchema
from sqlalchemy.orm import Session


class GenreService:
    """Genre service."""

    def __init__(self):
        pass

    @staticmethod
    def create_genre(db: Session, genre_schema: GenreCreateSchema) -> Genre:
        """Create new genre."""
        if genre_execute.get_genre_by_name(db, genre_schema.name):
            raise ValueError(f"Genre name `{genre_schema.name}` has existed.")
        new_genre = Genre(
            name=genre_schema.name,
        )
        return genre_execute.create_genre(db, genre=new_genre)

    @staticmethod
    def create_genres_bulk(db: Session, genre_schemas: List[GenreCreateSchema]) -> List[Genre]:
        """Bulk create genres."""
        new_genres = [Genre(name=genre_schema.name) for genre_schema in genre_schemas]
        return genre_execute.create_genres_bulk(db, new_genres)

    @staticmethod
    def get_genre(db: Session, genre_id: UUID) -> Genre:
        """Get genre."""
        return genre_execute.get_genre(db, genre_id)

    @staticmethod
    def get_genre_by_name(db: Session, genre_name: str) -> List[Genre]:
        """Get genre by name."""
        return genre_execute.get_genre_by_name(db, genre_name)

    @staticmethod
    def search_genres_by_name(db: Session, genre_name: str) -> List[Genre]:
        """Search genres by name."""
        return genre_execute.search_genres_by_name(db, genre_name)

    @staticmethod
    def get_all_genres(db: Session, offset: int = 0, limit: int = 100) -> List[Genre]:
        """Get all genre."""
        return genre_execute.get_all_genres(db, offset, limit)

    @staticmethod
    def update_genre(db: Session, update_info: dict) -> Genre:
        """Update genre."""
        return genre_execute.update_genre(
            db=db, genre_id=update_info.get("id", None), genre_name=update_info.get("name", None)
        )

    @staticmethod
    def delete_genre(db: Session, genre_id: UUID) -> Genre:
        """Delete genre."""
        return genre_execute.delete_genre(db, genre_id)


genre_service = GenreService()
