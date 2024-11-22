# pylint: disable=E0401
"""Track services."""

from typing import List

from api.database.execute import track as track_execute
from api.database.models import Track
from api.schemas.track import TrackCreateSchema
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


track_service = TrackService()
