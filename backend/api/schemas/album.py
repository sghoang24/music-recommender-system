# pylint: disable=E0401
"""Album schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AlbumCreateSchema(BaseModel):
    """Album create schema."""

    name: str = Field(..., description="Album name.")
    release_date: datetime = Field(..., description="Album release date.")


class AlbumUpdateSchema(BaseModel):
    """Album update schema."""

    id: UUID
    name: str = Field(..., description="Album name.")
    release_date: datetime = Field(..., description="Album release date.")


class AlbumSchema(BaseModel):
    """Album schema."""

    id: UUID
    name: str = Field(..., description="Album name.")
    release_date: Optional[datetime] = Field(..., description="Album release date.")
    created_at: datetime = Field(default=datetime.utcnow(), description="Timestamp of the first create.")
    updated_at: datetime = Field(default=datetime.utcnow(), description="Timestamp of the last update.")

    class Config:
        """Configuration."""

        from_attributes = True


class ListAlbumDisplay(BaseModel):
    """List album display."""

    total_albums: int
    albums: List[AlbumSchema]


class AlbumQuerySchema(BaseModel):
    """Album query schema."""

    offset: int = 0
    limit: int = 10
