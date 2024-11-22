# pylint: disable=E0401
"""Artist schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ArtistCreateSchema(BaseModel):
    """Artist create schema."""

    name: str = Field(..., description="Artist name.")
    nationality: Optional[str] = Field(..., description="Artist nationality.")
    birthday: Optional[datetime] = Field(..., description="Artist birthday.")


class ArtistUpdateSchema(BaseModel):
    """Artist update schema."""

    id: UUID
    name: str = Field(..., description="Artist name.")
    nationality: Optional[str] = Field(..., description="Artist nationality.")
    birthday: Optional[datetime] = Field(..., description="Artist birthday.")


class ArtistSchema(BaseModel):
    """Artist schema."""

    id: UUID
    name: str = Field(..., description="Artist name.")
    nationality: Optional[str] = Field(..., description="Artist nationality.")
    birthday: Optional[datetime] = Field(..., description="Artist birthday.")
    created_at: datetime = Field(default=datetime.utcnow(), description="Timestamp of the first create.")
    updated_at: datetime = Field(default=datetime.utcnow(), description="Timestamp of the last update.")

    class Config:
        """Configuration."""

        from_attributes = True


class ListArtistDisplay(BaseModel):
    """List artist display."""

    total_artists: int
    artists: List[ArtistSchema]
