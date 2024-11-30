# pylint: disable=E0401
"""Artist execute."""

from datetime import datetime
from typing import List
from uuid import UUID

from api.database.models import Artist
from api.schemas.artist import ArtistUpdateSchema
from sqlalchemy import orm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class ArtistRepository:
    """Artist Repository."""

    @staticmethod
    def create_artist(db: Session, artist: Artist) -> Artist:
        """Create artist."""
        db.add(artist)
        db.commit()
        db.refresh(artist)
        return artist

    @staticmethod
    def create_artists_bulk(db: Session, artists: List[Artist]) -> List[Artist]:
        """Bulk create artists."""
        db.add_all(artists)
        db.commit()
        for artist in artists:
            db.refresh(artist)
        return artists

    @staticmethod
    def get_artist(db: Session, artist_id: UUID) -> Artist:
        """Get artist."""
        return db.query(Artist).filter(Artist.id == artist_id).first()

    @staticmethod
    def get_artist_by_name(db: Session, artist_name: str) -> List[Artist]:
        """Get artist by name."""
        return db.query(Artist).filter(Artist.name == artist_name).first()

    @staticmethod
    def search_artists_by_name(db: Session, artist_name: str) -> List[Artist]:
        """Search artists by name."""
        return db.query(Artist).filter(Artist.name.ilike(f"%{artist_name}%")).all()

    @staticmethod
    def get_all_artists(db: Session, offset: int = 0, limit: int = 100) -> List[Artist]:
        """Get all artists with offset and limit."""
        query = db.query(Artist)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        query = query.options(orm.undefer(Artist.updated_at))
        return query.all()

    @staticmethod
    def update_artist(db: Session, update_info: ArtistUpdateSchema) -> Artist:
        """Update artists."""
        if artist_id := update_info.id:
            if artist := db.query(Artist).filter(Artist.id == artist_id).first():
                if updated_name := update_info.name:
                    artist.name = updated_name
                    artist.updated_at = datetime.utcnow()
                if updated_nationality := update_info.nationality:
                    artist.nationality = updated_nationality
                    artist.updated_at = datetime.utcnow()
                if updated_birthday := update_info.birthday:
                    artist.birthday = updated_birthday
                    artist.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(artist)
                return artist
        return None

    @staticmethod
    def delete_artist(db: Session, artist_id: UUID) -> Artist:
        """Delete artist."""
        try:
            if artist := db.query(Artist).filter(Artist.id == artist_id).first():
                db.delete(artist)
                db.commit()
                return artist

        except IntegrityError as e:
            # Handle any IntegrityError, such as foreign key violations here
            db.rollback()
            raise e


artist_execute = ArtistRepository()
