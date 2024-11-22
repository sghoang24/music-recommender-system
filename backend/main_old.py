# pylint: skip-file
from typing import Annotated, List

import auth
import models
import schemas
import services
from database import Base, SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(auth.router)

origins = [
    "https://music-recommender-phi.vercel.app",
    "http://localhost:3000",
    "https://d07e-2a09-bac5-d5cb-e6-00-17-325.ngrok-free.app",
]

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)


def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(db_session)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]


@app.get("/")
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"User": user}


# CRUD Tracks
@app.post("/tracks", status_code=status.HTTP_201_CREATED)
async def create_track(tracks: List[schemas.TrackSchema], db: db_dependency):
    try:
        created_tracks = []
        for track in tracks:
            existing_track = db.query(models.Track).filter(models.Track.id == track.id).first()
            if existing_track:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Track already exists: " + str(existing_track.id)
                )
            new_track = models.Track(**track.model_dump())
            db.add(new_track)
            db.commit()
            db.refresh(new_track)
            created_tracks.append(new_track)
        return {"message": "Tracks created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating tracks: " + str(e)
        )


@app.get("/tracks/{track_id}", response_model=schemas.TrackSchema)
async def get_track(track_id: str, db: db_dependency):
    print(track_id)
    track = db.query(models.Track).filter(models.Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track


@app.put("/tracks/{track_id}", response_model=schemas.TrackSchema)
async def update_track(track_id: str, update_data: schemas.TrackUpdateSchema, db: db_dependency):
    # check if track exists
    existing_track = db.query(models.Track).filter(models.Track.id == track_id).first()
    if not existing_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    print(existing_track)
    for key, value in update_data.model_dump().items():
        setattr(existing_track, key, value)

    try:
        db.commit()
        db.refresh(existing_track)
        return existing_track
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating track: " + str(e))


@app.delete("/tracks/{track_id}")
async def delete_track(track_id: str, db: db_dependency):
    # check if tracks exists
    existing_track = db.query(models.Track).filter(models.Track.id == track_id).first()
    if not existing_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

    db.delete(existing_track)
    db.commit()

    return {"message": "Track deleted successfully"}


@app.get("/get_10_tracks/", response_model=List[schemas.TrackSchema])
async def get_random_tracks(db: db_dependency):
    tracks = db.query(models.Track).order_by(func.random()).limit(10).all()

    return tracks


@app.get("/get_track_by_id/{track_id}", response_model=schemas.TrackSchema)
async def get_track_by_id(track_id: str, db: db_dependency):
    track = db.query(models.Track).filter(models.Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track


@app.get("/search_tracks", response_model=List[schemas.TrackSchema])
async def search_tracks(search_query: str, genres: str, db: db_dependency):
    try:
        tracks = await services.search_tracks(search_query=search_query, genres=genres, db=db)
    except Exception as e:
        # return []
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error searching tracks: " + str(e)
        )

    return tracks


@app.post("/like_track")
async def like_track(liked_tracks_schema: schemas.LikedTracksSchema, db: db_dependency):
    liked_track = await services.create_liked_track(
        track_id=liked_tracks_schema.track_id, user_id=liked_tracks_schema.user_id, db=db
    )

    if not liked_track:
        raise HTTPException(status_code=400, detail="Failed to like track")
    return liked_track


@app.post("/check_like")
async def check_like(liked_tracks_schema: schemas.LikedTracksSchema, db: db_dependency):
    is_liked = await services.check_liked_tracks(
        track_id=liked_tracks_schema.track_id, user_id=liked_tracks_schema.user_id, db=db
    )
    # if not is_liked:
    #     raise HTTPException(status_code=404, detail="Failed to check like track")
    return {"is_liked": is_liked}


@app.post("/unlike_track")
async def unlike_track(liked_tracks_schema: schemas.LikedTracksSchema, db: db_dependency):
    message = await services.delete_liked_track(
        track_id=liked_tracks_schema.track_id, user_id=liked_tracks_schema.user_id, db=db
    )
    if not message:
        raise HTTPException(status_code=400, detail="Failed to unlike track")
    return message


@app.get("/get_liked_tracks/{user_id}", response_model=List[schemas.TrackSchema])
async def get_liked_tracks(user_id: int, db: db_dependency):
    liked_tracks = await services.get_liked_tracks(user_id=user_id, db=db)
    if not liked_tracks:
        raise HTTPException(status_code=404, detail="Failed to get liked tracks")
    return liked_tracks


# Recommendation
@app.get("/get_recommendation/{track_id}", response_model=List[schemas.TrackSchema])
async def get_recommendation(track_id: str, db: db_dependency):
    recommended_tracks = await services.get_recommendation(track_id=track_id, db=db)
    if not recommended_tracks:
        raise HTTPException(status_code=404, detail="Failed to get recommendation")
    return recommended_tracks


@app.get("/get_recommendation_by_likes/{user_id}", response_model=List[schemas.TrackSchema])
async def get_recommendation_by_likes(user_id: int, db: db_dependency):
    recommended_tracks = await services.get_recommendation_by_likes(user_id=user_id, db=db)
    if not recommended_tracks:
        raise HTTPException(status_code=404, detail="Failed to get recommendation by likes")
    return recommended_tracks


@app.get("/get_tracks_by_preferences/{user_id}", response_model=List[schemas.TrackSchema])
async def get_tracks_by_preferences(user_id: int, db: db_dependency):
    tracks = await services.get_tracks_by_preferences(user_id=user_id, db=db)
    if not tracks:
        raise HTTPException(status_code=404, detail="Failed to get recommendation by preferences")
    return tracks


@app.get("/get_tracks_for_user/{user_id}", response_model=List[schemas.TrackSchema])
async def get_tracks_for_user(user_id: int, db: db_dependency):
    tracks = await services.get_tracks_for_user(user_id=user_id, db=db)
    if not tracks:
        raise HTTPException(status_code=404, detail="Failed to get tracks for user")
    return tracks
