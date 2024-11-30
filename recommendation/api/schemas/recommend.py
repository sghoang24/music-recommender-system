# pylint: disable=E0401
"""Recommend schemas."""

from typing import List, Optional

from pydantic import BaseModel, Field


class RecommendInputSchema(BaseModel):
    """Rcommendatio input schema."""

    track_id: str = Field(..., description="Unique identifier of track.")
    existed_ids: Optional[List[str]] = Field(..., description="List existed ids.")
