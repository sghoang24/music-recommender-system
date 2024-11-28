# pylint: disable=E0401
"""LikedTrack services."""

from typing import List

from api.database.execute import liked_track as liked_track_execute
from api.database.models import LikedTrack
from api.schemas.liked_track import LikedTrackCreateSchema
from sqlalchemy.orm import Session


class LikedTrackService:
    """Liked Track service."""

    def __init__(self):
        pass

    @staticmethod
    def create_liked_track(db: Session, like_track_schema: LikedTrackCreateSchema) -> LikedTrack:
        """Create new liked track."""
        new_track = LikedTrack(
            user_id=like_track_schema.user_id,
            track_id=like_track_schema.track_id,
        )
        return liked_track_execute.create_liked_track(db, liked_track=new_track)

    @staticmethod
    def create_liked_tracks_bulk(db: Session, like_track_schemas: List[LikedTrackCreateSchema]) -> List[LikedTrack]:
        """Bulk create liked tracks."""
        new_tracks = [
            LikedTrack(
                user_id=like_track_schema.user_id,
                track_id=like_track_schema.track_id,
            )
            for like_track_schema in like_track_schemas
        ]
        return liked_track_execute.create_liked_tracks_bulk(db, new_tracks)


liketrack_service = LikedTrackService()
