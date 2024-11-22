# pylint: disable=E0401
"""Genre execute."""

from datetime import datetime
from typing import List
from uuid import UUID

from api.database.models import Genre
from sqlalchemy import orm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def create_genre(db: Session, genre: Genre) -> Genre:
    """Create genre."""
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre


def create_genres_bulk(db: Session, genres: List[Genre]) -> List[Genre]:
    """Bulk create genres."""
    db.add_all(genres)
    db.commit()
    for genre in genres:
        db.refresh(genre)
    return genres


def get_genre(db: Session, genre_id: UUID) -> Genre:
    """Get genre."""
    return db.query(Genre).filter(Genre.id == genre_id).first()


def get_genre_by_name(db: Session, genre_name: str) -> List[Genre]:
    """Get genre by name."""
    return db.query(Genre).filter(Genre.name == genre_name).first()


def search_genres_by_name(db: Session, genre_name: str) -> List[Genre]:
    """Search genres by name."""
    return db.query(Genre).filter(Genre.name.like(f"%{genre_name}%")).all()


def get_all_genres(db: Session, offset: int = 0, limit: int = 100) -> List[Genre]:
    """Get all genres with offset and limit."""
    query = db.query(Genre)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    query = query.options(orm.undefer(Genre.updated_at))
    return query.all()


def update_genre(db: Session, genre_id: UUID, genre_name: str) -> Genre:
    """Update genre."""
    if genre_id and genre_name:
        if genre := db.query(Genre).filter(Genre.id == genre_id).first():
            genre.name = genre_name
            genre.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(genre)
            return genre


def delete_genre(db: Session, genre_id: UUID) -> Genre:
    """Delete genre."""
    try:
        if genre := db.query(Genre).filter(Genre.id == genre_id):
            db.delete(genre)
            db.commit()
            return genre

    except IntegrityError as e:
        # Handle any IntegrityError, such as foreign key violations here
        db.rollback()
        raise e
