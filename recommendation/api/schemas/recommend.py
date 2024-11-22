# pylint: disable=E0401
"""Recommend schemas."""

from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class RecommendInputSchema(BaseModel):
    """Rcommendatio input schema."""

    track_id: UUID = Field(..., description="Unique identifier of track.")
    existed_ids: List[UUID] = Field(..., description="List existed ids.")
