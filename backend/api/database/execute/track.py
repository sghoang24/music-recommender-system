# pylint: disable=E0401
"""Track execute."""

import random
from typing import List
from uuid import UUID

from api.database.execute import artist as artist_execute
from api.database.execute import genre as genre_execute
from api.database.models import Album, Artist, Genre, Track, User
from api.helpers.utils import get_recommendation, get_tags_keywords
from api.schemas.track import ListTrackDisplay, TrackDisplay
from core.config import GENRES_MAP
from sqlalchemy import func, or_, orm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def create_track(db: Session, track: Track) -> Track:
    """Create new track."""
    db.add(track)
    db.commit()
    db.refresh(track)
    return track


def create_tracks_bulk(db: Session, tracks: List[Track]) -> List[Track]:
    """Bulk create tracks."""
    db.add_all(tracks)
    db.commit()
    for track in tracks:
        db.refresh(track)
    return tracks


def get_track(db: Session, track_id: UUID) -> Track:
    """Get track."""
    return db.query(Track).filter(Track.id == track_id).first()


def get_all_tracks(db: Session, offset: int = 0, limit: int = 100) -> List[Track]:
    """Get all tracks with offset and limit."""
    query = db.query(Track)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    query = query.options(orm.undefer(Track.updated_at))
    return query.all()


def get_tracks_by_user_preferences(db: Session, user_id: UUID, limit: int = 100):
    """Get tracks by user preferences."""
    user = db.query(User).filter(User.id == user_id).first()
    all_genres = genre_execute.get_all_genres(db=db, offset=0, limit=None)
    all_genre_ids = [genre.id for genre in all_genres if genre.name in user.preferences]
    track = db.query(Track).filter(Track.genre_id.in_(all_genre_ids)).order_by(func.random)
    if limit:
        track = track.limit(limit)
    return track.all()


def get_random_tracks(db: Session, limit: int = 10) -> List[Track]:
    """Get random tracks with limit."""
    all_ids = db.query(Track.id).all()
    if not all_ids:
        return []

    random_ids = random.sample([id[0] for id in all_ids], min(limit, len(all_ids)))
    return db.query(Track).order_by(Track.id.in_(random_ids)).all()


def search_tracks(db: Session, query: str, genres: str, limit: int = 100):
    """Search tracks."""
    if genres.lower() != "all":
        genres = genres.split(",")
        genres = [GENRES_MAP[genre] for genre in genres]
    search_artists = artist_execute.get_artists_by_name(db=db, artist_name=query)
    search_artist_ids = [artist.id for artist in search_artists]
    tracks = db.query(Track).filter(or_(Track.title.like(f"%{query}%"), Track.artist_id.in_(search_artist_ids)))

    if genres.lower() != "All":
        all_genres = genre_execute.get_all_genres(db=db, offset=0, limit=None)
        all_genre_ids = [genre.id for genre in all_genres if genre.name in genres]
        tracks = tracks.filter(Track.genre_id.in_(all_genre_ids))
    if limit:
        tracks = tracks.limit(limit)
    return tracks.all()


def delete_track(db: Session, track_id: UUID) -> Track:
    """Delete track."""
    try:
        if track := db.query(Track).filter(Track.id == track_id):
            db.delete(track)
            db.commit()
            return track

    except IntegrityError as e:
        # Handle any IntegrityError, such as foreign key violations here
        db.rollback()
        raise e


async def get_track_recommendation(db: Session, track_id: UUID):
    """Get track recommendation."""
    original_track = db.query(Track).filter(Track.id == track_id).first()
    original_tags = get_tags_keywords(original_track.tags)

    # Get the recommended tracks
    title_count = {}
    duplicated_ids = []
    detect_duplicated = True

    while detect_duplicated:
        detect_duplicated = False
        track_ids = await get_recommendation(track_id=track_id, existed_ids=duplicated_ids)
        tracks = (
            db.query(
                Track.id.label("id"),
                Track.title.label("title"),
                Album.name.label("album"),
                Artist.name.label("artist"),
                Genre.name.label("genre"),
                Track.cover_art.label("cover_art"),
                Track.mp3_url.label("mp3_url"),
                Track.tags.label("tags"),
                Album.release_date.label("release_date"),
            )
            .join(Album, Album.id == Track.album_id)
            .join(Artist, Artist.id == Track.artist_id)
            .join(Genre, Genre.id == Track.genre_id)
            .filter(Track.id.in_(track_ids))
            .all()
        )
        for track in tracks:
            title = track.title
            # Detect duplicates
            if title in title_count:
                duplicated_ids.append(track.id)
                detect_duplicated = True
            else:
                title_count[title] = 1

        if detect_duplicated:
            # Reset title count
            title_count = {}
            continue

    for track in tracks:
        track.tags = get_tags_keywords(track.tags)
        track.tags = list(set(track.tags) & set(original_tags))

    display_tracks = [
        TrackDisplay(
            id=track.id,
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
    return ListTrackDisplay(total_entries=len(display_tracks), lisk_tracks=display_tracks)
