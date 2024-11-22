# pylint: disable=E0401
"""User Model."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, validate_email


class UserCreateSchema(BaseModel):
    """Schema for creating a user."""

    email: str = Field(..., description="Email address of the user.")
    password: str = Field(..., description="Password for the user.")
    full_name: Optional[str] = Field(None, omit_default=True, description="Full name of the user.")
    role: int = Field(0, description="Role of user.")
    preferences: Optional[List[str]] = Field([], description="User's description.")

    @field_validator("email", mode="before")
    def user_validate_email(cls, value: str) -> str:
        """User validate email."""
        _, email = validate_email(value)
        return email.lower()


class UserSchema(BaseModel):
    """Schema for representing a user."""

    id: UUID
    email: str
    is_active: bool
    role: int = Field(0, description="Role of user.")
    preferences: Optional[List[str]] = Field([], description="User's description.")
    created_at: datetime = Field(default=datetime.utcnow(), description="Timestamp of the first create.")
    updated_at: datetime = Field(default=datetime.utcnow(), description="Timestamp of the last update.")

    class Config:
        """Configuration."""

        from_attributes = True
