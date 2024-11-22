# pylint: disable=E0401
# pylint: skip-file
"""Token Models."""
from typing import Optional as Op

from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Model for representing an access token."""

    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    """Schema for representing token data."""

    email: Op[str] = None
