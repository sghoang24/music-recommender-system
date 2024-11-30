# pylint: disable=E0401
"""LikedTrack services."""

from typing import List

from api.database.execute.liked_track import liked_track_execute
from api.database.models import LikedTrack
from api.schemas.liked_track import (
    LikedTrackCreateSchema,
    LikedTrackGetSchema,
)
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

    @staticmethod
    def get_liked_track(db: Session, liked_track_schema: LikedTrackCreateSchema):
        """Get liked track."""
        return liked_track_execute.get_liked_track(
            db=db,
            user_id=liked_track_schema.user_id,
            track_id=liked_track_schema.track_id,
        )

    @staticmethod
    def get_liked_tracks_by_user(db: Session, liked_track_schema: LikedTrackGetSchema):
        """Get liked track."""
        return liked_track_execute.get_liked_tracks_by_user(
            db=db,
            user_id=liked_track_schema.user_id,
            offset=liked_track_schema.offset,
            limit=liked_track_schema.limit,
        )

    @staticmethod
    def delete_liked_track(db: Session, liked_track_schema: LikedTrackCreateSchema):
        """Delete liked track."""
        return liked_track_execute.delete_liked_track(
            db=db,
            user_id=liked_track_schema.user_id,
            track_id=liked_track_schema.track_id,
        )


liketrack_service = LikedTrackService()
