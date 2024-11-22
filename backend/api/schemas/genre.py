# pylint: disable=E0401
"""Genre schemas."""

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class GenreCreateSchema(BaseModel):
    """Genre create schema."""

    name: str = Field(..., description="Genre name.")


class GenreUpdateSchema(BaseModel):
    """Genre update schema."""

    id: UUID
    name: str = Field(..., description="Genre name.")


class GenreSchema(BaseModel):
    """Genre schema."""

    id: UUID
    name: str = Field(..., description="Genre name.")
    created_at: datetime = Field(default=datetime.utcnow(), description="Timestamp of the first create.")
    updated_at: datetime = Field(default=datetime.utcnow(), description="Timestamp of the last update.")

    class Config:
        """Configuration."""

        from_attributes = True


class ListGenreDisplay(BaseModel):
    """List genre display."""

    total_genres: int
    genres: List[GenreSchema]
