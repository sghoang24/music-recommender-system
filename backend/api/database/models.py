# pylint: disable=E0401
"""DB models."""

import enum
import uuid

import pydantic
from api.database.connection import Database
from core.constant import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER
from logger.logger import custom_logger
from sqlalchemy import ARRAY, UUID, Boolean, Column, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Session

custom_logger.info("Connecting PostgreSQL Database.")
POSTGRES_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
db = Database(POSTGRES_DATABASE_URL)
Base = db.Base


def db_session() -> Session:
    """Provide a thread-safe session."""
    session_db = db.SessionLocal()
    try:
        yield session_db
    finally:
        session_db.close()


custom_logger.info("Connect to PostgreSQL Database Success.")


class BaseModel(Base):
    """Base model."""

    __abstract__ = True

    created_at = Column(name="created_at", type_=DateTime(timezone=True), server_default=func.now())
    updated_at = Column(name="updated_at", type_=DateTime(timezone=True), server_default=func.now())

    @classmethod
    def create_from_schema(cls, schema: pydantic.BaseModel):
        """Create from schema."""
        obj = cls()
        obj.update_from_schema(schema)
        return obj

    def update_from_schema(self, schema: pydantic.BaseModel):
        """Update from schema."""
        for attr, value in schema.__dict__.items():
            if value is None:
                continue
            if attr != "_sa_instance_state":
                if isinstance(value, enum.Enum):
                    value = value.value
                if isinstance(value, list):
                    value = [x.value if isinstance(x, enum.Enum) else x for x in value]
                setattr(self, attr, value)

    def as_dict(self):
        """Convert to dictionary."""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class User(BaseModel):
    """User."""

    __tablename__ = "user"

    id = Column(name="id", type_=UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(name="email", type_=String, unique=True, index=True)
    hashed_password = Column(name="password", type_=String)
    is_active = Column(name="is_active", type_=Boolean, default=False)
    full_name = Column(name="full_name", type_=String)
    role = Column(name="role", type_=Integer, default=0)
    preferences = Column(name="preferences", type_=ARRAY(String), default=[])


class Artist(BaseModel):
    """Artist."""

    __tablename__ = "artist"

    id = Column(name="id", type_=UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(name="artist_name", type_=String)
    nationality = Column(name="nationality", type_=String)
    birthday = Column(name="birthday", type_=Date)


class Genre(BaseModel):
    """Genre."""

    __tablename__ = "genre"

    id = Column(name="id", type_=UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(name="name", type_=String)


class Album(BaseModel):
    """Album."""

    __tablename__ = "album"

    id = Column(name="id", type_=UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(name="name", type_=String)
    release_date = Column(name="release_date", type_=DateTime(timezone=False), server_default=func.now())


class Track(BaseModel):
    """Track."""

    __tablename__ = "track"

    id = Column(name="id", type_=UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(name="title", type_=String)
    artist_id = Column(ForeignKey("artist.id"))
    genre_id = Column(ForeignKey("genre.id"))
    album_id = Column(ForeignKey("album.id"))
    cover_art = Column(name="cover_art", type_=String)
    mp3_url = Column(name="mp3_url", type_=String)
    tags = Column(name="tags", type_=ARRAY(String), default=[])


class LikedTrack(BaseModel):
    """Liked track."""

    __tablename__ = "liked_track"

    id = Column(name="id", type_=UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("user.id"))
    track_id = Column(ForeignKey("track.id", ondelete="CASCADE"))
