# pylint: disable=E0401
"""Process and import data."""

import os
import sys

code_root = os.path.abspath(os.path.join(__file__, "../.."))
print(f"sys_root = {code_root}")
if code_root not in sys.path:
    sys.path.append(code_root)

import pandas as pd
from api.database.execute import delete_all
from api.database.models import Album, Artist, Genre, Track, db
from api.schemas.album import AlbumCreateSchema
from api.schemas.artist import ArtistCreateSchema
from api.schemas.genre import GenreCreateSchema
from api.schemas.track import TrackCreateSchema
from api.services.album_service import album_service
from api.services.artist_service import artist_service
from api.services.genre_service import genre_service
from api.services.track_service import track_service
from pandas import DataFrame
from sqlalchemy.orm import Session
from tqdm import tqdm


def process_data(db: Session, df: DataFrame):
    """Process data."""
    delete_all(db, Track)
    delete_all(db, Album)
    delete_all(db, Artist)
    delete_all(db, Genre)
    print("Delete all data done...")

    artists = list(df["artist"].unique())
    genres = list(df["genre"].unique())
    albums = list(df[["album", "release_date"]].drop_duplicates().itertuples(index=False, name=None))
    batch_size = 100
    album_id_map, artist_id_map, genre_id_map = {}, {}, {}
    for idx in range(0, len(albums), batch_size):
        album_list = [
            AlbumCreateSchema(name=name, release_date=release_date)
            for name, release_date in albums[idx : idx + batch_size]
        ]
        created_albums = album_service.create_albums_bulk(db, album_list)
        album_id_map.update({album.name: album.id for album in created_albums})
    print("Done save albums...")

    for idx in range(0, len(genres), batch_size):
        genre_list = [GenreCreateSchema(name=name) for name in genres[idx : idx + batch_size]]
        created_genres = genre_service.create_genres_bulk(db, genre_list)
        genre_id_map.update({genre.name: genre.id for genre in created_genres})
    print("Done save genres...")

    for idx in range(0, len(artists), batch_size):
        artist_list = [
            ArtistCreateSchema(
                name=name,
                nationality=None,
                birthday=None,
            )
            for name in artists[idx : idx + batch_size]
        ]
        created_artists = artist_service.create_artists_bulk(db, artist_list)
        artist_id_map.update({artist.name: artist.id for artist in created_artists})
    print("Done save artists...")

    # df = df.drop(columns=['album', 'artist', 'genre'])
    track_list = []
    progress_bar = tqdm(df.iterrows(), desc="Import data", total=len(df))
    for index, row in progress_bar:
        progress_bar.set_description(row["title"])
        track_list.append(
            TrackCreateSchema(
                title=row["title"],
                album_id=album_id_map[row["album"]],
                artist_id=artist_id_map[row["artist"]],
                genre_id=genre_id_map[row["genre"]],
                mp3_url=row["mp3_url"],
                cover_art=row["cover_art"],
                tags=row["tags"],
            )
        )
        if index % 100 == 0:
            _ = track_service.create_tracks_bulk(db, track_list)
            track_list = []
    return df


def extract_tags(tag_string: str):
    """Extract tags."""
    if not isinstance(tag_string, str) or not tag_string:
        return []
    return [item.split(": ")[0].strip() for item in tag_string.split(", ")]


def import_data():
    """Import data."""
    df = pd.read_csv("tracks_rows.csv")
    df["tags"] = df["tags"].apply(extract_tags)
    df = process_data(db.SessionLocal(), df)


if __name__ == "__main__":
    import_data()
