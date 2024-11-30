# pylint: disable=E0401
"""Track services."""

from typing import List
from uuid import UUID

from api.database.execute.track import track_execute
from api.database.models import Track
from api.schemas.track import TrackCreateSchema, TrackUpdateSchema
from sqlalchemy.orm import Session


class TrackService:
    """Track service."""

    def __init__(self):
        pass

    @staticmethod
    def create_track(db: Session, track_schema: TrackCreateSchema) -> Track:
        """Create new track."""
        new_track = Track(**track_schema.dict())
        return track_execute.create_track(db, track=new_track)

    @staticmethod
    def create_tracks_bulk(db: Session, track_schemas: List[TrackCreateSchema]) -> List[Track]:
        """Bulk create tracks."""
        new_tracks = [Track(**track_schema.dict()) for track_schema in track_schemas]
        return track_execute.create_tracks_bulk(db, new_tracks)
    
    @staticmethod
    def get_all_tracks(db: Session, offset: int, limit: int) -> List[Track]:
        """Get all tracks."""
        return track_execute.get_all_tracks(db, offset, limit)
    
    @staticmethod
    def get_track(db: Session, track_id: int) -> Track:
        """Get track."""
        return track_execute.get_track(db, track_id)
    
    @staticmethod
    def get_random_tracks(db: Session, limit: int) -> List[Track]:
        """Get random tracks."""
        return track_execute.get_random_tracks(db, limit)
    
    @staticmethod
    def get_track_by_artist(db: Session, artist_id: int, limit: int = 10) -> List[Track]:
        """Get track by artist."""
        return track_execute.get_track_by_artist(db, artist_id, limit)
    
    @staticmethod
    def update_track(db: Session, track_update: TrackUpdateSchema) -> Track:
        """Update track."""
        track_id = track_update.id
        track_data = track_update.dict(exclude={"id"})
        return track_execute.update_track(db=db, track_id=track_id, track=track_data)

    @staticmethod
    def delete_track(db: Session, track_id: int) -> Track:
        """Delete track."""
        return track_execute.delete_track(db, track_id)

    @staticmethod
    def get_track_by_name(db: Session, track_name: str) -> List[Track]:
        """Search tracks by name."""
        return track_execute.get_track_by_name(db, track_name)

    @staticmethod
    def search_tracks(db: Session, search_query: str, genres: str) -> List[Track]:
        """Search tracks by name."""
        return track_execute.search_tracks(db, search_query, genres)

    @staticmethod
    async def get_tracks_by_user_preferences(db: Session, user_id: UUID, limit: int = 50):
        """Get tracks by user preferences."""
        return await track_execute.get_tracks_by_user_preferences(db, user_id, limit)

    @staticmethod
    async def get_recommendation_by_likes(db: Session, user_id: UUID):
        """Get recommendation tracks by likes."""
        return await track_execute.get_recommendation_by_likes(db, user_id)

    @staticmethod
    async `def get_recommendation_by_track(db: Session, track_id: UUID):
        """Get recommendation tracks by tracks."""
        return await track_execute.get_recommendation_by_track(db, track_id)`

    @staticmethod
    async def get_recommendation_by_user(db: Session, user_id: UUID, limit: int = 50):
        """Get recommendation tracks by user."""
        return await track_execute.get_recommendation_by_user(db, user_id, limit)


track_service = TrackService()
