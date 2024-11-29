# pylint: disable=E0401
"""LikeTrack execute."""

from typing import List
from uuid import UUID

from api.database.models import Album, Artist, Genre, LikedTrack, Track
from api.schemas.liked_track import LikedTrackDisplay, ListLikedTrackDisplay
from sqlalchemy.orm import Session


def create_liked_track(db: Session, liked_track: LikedTrack) -> LikedTrack:
    """Create new liked track."""
    db.add(liked_track)
    db.commit()
    db.refresh(liked_track)
    return liked_track


def create_liked_tracks_bulk(db: Session, liked_tracks: List[LikedTrack]) -> List[LikedTrack]:
    """Bulk create liked tracks."""
    db.add_all(liked_tracks)
    db.commit()
    for liked_track in liked_tracks:
        db.refresh(liked_track)
    return liked_tracks


def get_liked_track(db: Session, user_id: UUID, track_id: UUID) -> LikedTrack:
    """Get liked track."""
    return (
        db.query(LikedTrack)
        .filter(
            LikedTrack.user_id == user_id,
            LikedTrack.track_id == track_id,
        )
        .first()
    )


def get_liked_tracks_by_user(db: Session, user_id: UUID, offset: int = 0, limit: int = 100):
    """Get liked tracks by user."""
    tracks = (
        db.query(
            Track.title.label("title"),
            Track.cover_art.label("cover_art"),
            Track.mp3_url.label("mp3_url"),
            Track.tags.label("tags"),
            Album.release_date.label("release_date"),
            Album.name.label("album"),
            Artist.name.label("artist"),
            Genre.name.label("genre"),
        )
        .join(LikedTrack, LikedTrack.track_id == Track.id)
        .join(Album, Album.id == Track.album_id)
        .join(Artist, Artist.id == Track.artist_id)
        .join(Genre, Genre.id == Track.genre_id)
        .filter(LikedTrack.user_id == user_id)
    )
    if offset:
        tracks = tracks.offset(offset)
    if limit:
        tracks = tracks.limit(limit)
    tracks = tracks.all()
    liked_track = [
        LikedTrackDisplay(
            title=track.title,
            artist=track.artist,
            genre=track.genre,
            album=track.album,
            cover_art=track.cover_art,
            mp3_url=track.mp3_url,
            tags=track.tags,
            release_date=track.release_date,
        )
        for track in tracks
    ]
    return ListLikedTrackDisplay(total_entries=len(liked_track), lisk_liked_tracks=liked_track)


def delete_liked_track(db: Session, user_id: UUID, track_id: UUID) -> LikedTrack:
    """Delete liked track."""
    if liked_track := (
        db.query(LikedTrack)
        .filter(
            LikedTrack.user_id == user_id,
            LikedTrack.track_id == track_id,
        )
        .first()
    ):
        db.delete(liked_track)
        db.commit()
        return liked_track
