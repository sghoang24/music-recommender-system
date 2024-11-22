# pylint: disable=E0401
"""Album execute."""

from datetime import datetime
from typing import List
from uuid import UUID

from api.database.models import Album
from api.schemas.album import AlbumUpdateSchema
from sqlalchemy import orm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def create_album(db: Session, album: Album) -> Album:
    """Create album."""
    db.add(album)
    db.commit()
    db.refresh(album)
    return album


def create_albums_bulk(db: Session, albums: List[Album]) -> List[Album]:
    """Bulk create albums."""
    db.add_all(albums)
    db.commit()
    for album in albums:
        db.refresh(album)
    return albums


def get_album(db: Session, album_id: UUID) -> Album:
    """Get album."""
    return db.query(Album).filter(Album.id == album_id).first()


def get_album_by_name(db: Session, album_name: str) -> List[Album]:
    """Get albums by name."""
    return db.query(Album).filter(Album.name == album_name).first()


def search_albums_by_name(db: Session, album_name: str) -> List[Album]:
    """Search albums by name."""
    return db.query(Album).filter(Album.name.like(f"%{album_name}%")).all()


def get_all_albums(db: Session, offset: int = 0, limit: int = 100) -> List[Album]:
    """Get all albums with offset and limit."""
    query = db.query(Album)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    query = query.options(orm.undefer(Album.updated_at))
    return query.all()


def update_album(db: Session, update_info: AlbumUpdateSchema) -> Album:
    """Update album."""
    if album_id := update_info.id:
        if album := db.query(Album).filter(Album.id == album_id).first():
            if updated_name := update_info.name:
                album.name = updated_name
                album.updated_at = datetime.utcnow()
            if updated_release_date := update_info.release_date:
                album.release_date = updated_release_date
                album.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(album)
            return album
    return None


def delete_album(db: Session, album_id: UUID) -> Album:
    """Delete album."""
    try:
        if album := db.query(Album).filter(Album.id == album_id):
            db.delete(album)
            db.commit()
            return album

    except IntegrityError as e:
        # Handle any IntegrityError, such as foreign key violations here
        db.rollback()
        raise e
