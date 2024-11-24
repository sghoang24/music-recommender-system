# pylint: disable=E0401
"""API Routes."""

from api.routes import (
    album_route,
    artist_route,
    authentication_route,
    genre_route,
    liketrack_route,
    track_route,
    user_route,
)
from fastapi import APIRouter

app = APIRouter()

app.include_router(authentication_route.router, tags=["Authentication"])
app.include_router(user_route.router, tags=["User"], prefix="/user")
app.include_router(album_route.router, tags=["Album"], prefix="/album")
app.include_router(artist_route.router, tags=["Artist"], prefix="/artist")
app.include_router(genre_route.router, tags=["Genre"], prefix="/genre")
app.include_router(track_route.router, tags=["Track"], prefix="/track")
app.include_router(liketrack_route.router, tags=["Liked Track"], prefix="/likedtrack")
