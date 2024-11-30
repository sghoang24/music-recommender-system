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


class LikedTrackGetSchema(BaseModel):
    """Liked Track Get Schema."""

    user_id: UUID = Field(..., description="Unique identifier of user.")
    offset: Optional[int] = Field(0, description="Offset.")
    limit: Optional[int] = Field(50, description="Limit.")


class LikedTrackDisplay(BaseModel):
    """Liked Track schema."""

    id: UUID = Field(..., description="Unique identifier of track.")
    title: str
    artist: str = Field(..., description="Artist name.")
    genre: str = Field(..., description="Genre name.")
    album: str = Field(..., description="Album name.")
    cover_art: Optional[str]
    mp3_url: Optional[str]
    tags: Optional[List[str]] = Field(..., description="Tags")
    release_date: Optional[datetime] = Field(..., description="Track release date")


class ListLikedTrackDisplay(BaseModel):
    """List liked track."""

    total_entries: int
    list_liked_tracks: List[LikedTrackDisplay]
