# pylint: disable=E0401
"""Track schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TrackCreateSchema(BaseModel):
    """Track create schema."""

    title: str
    artist_id: UUID = Field(..., description="Artist unique identifier.")
    genre_id: UUID = Field(..., description="Genre unique identifier.")
    album_id: UUID = Field(..., description="Album unique identifier.")
    cover_art: Optional[str]
    mp3_url: Optional[str]
    tags: Optional[List[str]] = Field(..., description="Tags")


class TrackDisplay(BaseModel):
    """Track display schema."""

    id: UUID
    title: str
    artist: str = Field(..., description="Artist name.")
    genre: str = Field(..., description="Genre name.")
    album: str = Field(..., description="Album name.")
    cover_art: Optional[str]
    mp3_url: Optional[str]
    tags: Optional[List[str]] = Field(..., description="Tags")
    release_date: Optional[datetime] = Field(..., description="Track release date")

    class Config:
        """Configuration."""

        from_attributes = True


class ListTrackDisplay(BaseModel):
    """List track display."""

    total_entries: int
    list_tracks: List[TrackDisplay]
    
class TrackUpdateSchema(BaseModel):
    """Track update schema."""
    id : UUID
    title: Optional[str] = Field(None, description="Title of the track.")
    artist_id: Optional[UUID] = Field(None, description="Artist unique identifier.")
    genre_id: Optional[UUID] = Field(None, description="Genre unique identifier.")
    album_id: Optional[UUID] = Field(None, description="Album unique identifier.")
    cover_art: Optional[str] = Field(None, description="URL of the cover art.")
    mp3_url: Optional[str] = Field(None, description="URL of the MP3 file.")
    tags: Optional[List[str]] = Field(None, description="Tags for the track.")
    
    class Config:
        """Configuration."""

        from_attributes = True
