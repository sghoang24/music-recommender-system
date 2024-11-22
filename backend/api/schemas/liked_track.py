# pylint: disable=E0401
"""Liked Track Schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class LikedTrackCreateSchema(BaseModel):
    """Liked Track Create Schema."""

    user_id: UUID = Field(..., description="Unique identifier of user.")
    track_id: UUID = Field(..., description="Unique identifier of track.")


class LikedTrackDisplay(BaseModel):
    """Liked Track schema."""

    title: str
    artist: str = Field(..., description="Artist name.")
    genre: str = Field(..., description="Genre name.")
    album: str = Field(..., description="Album name.")
    cover_art: Optional[str]
    mp3_url: Optional[str]
    tags: Optional[str] = Field(..., description="Tags")
    release_date: Optional[datetime] = Field(..., description="Track release date")


class ListLikedTrackDisplay(BaseModel):
    """List liked track."""

    total_entries: int
    lisk_liked_tracks: List[LikedTrackDisplay]
