"""
Genres API routes
"""

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app import crud
from app.models import (
    Genre, GenreCreate, GenrePublic, GenresPublic,
    Song, SongsPublic,
    Album, AlbumsPublic,
    Message,
)

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("/", response_model=GenresPublic)
def read_genres(session: SessionDep) -> Any:
    """
    Retrieve all genres.
    """
    genres = crud.get_genres(session=session)
    count = len(genres)
    return GenresPublic(data=genres, count=count)


@router.get("/{genre_id}", response_model=GenrePublic)
def read_genre(session: SessionDep, genre_id: uuid.UUID) -> Any:
    """
    Get genre by ID.
    """
    genre = crud.get_genre(session=session, genre_id=genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=GenrePublic)
def create_genre(
    *, session: SessionDep, current_user: CurrentUser, genre_in: GenreCreate
) -> Any:
    """
    Create new genre.
    Only superusers can create genres.
    """
    # Check if genre already exists
    existing = crud.get_genre_by_name(session=session, name=genre_in.name)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Genre with this name already exists"
        )
    
    genre = crud.create_genre(session=session, genre_create=genre_in)
    return genre


@router.get("/{genre_id}/songs", response_model=SongsPublic)
def read_genre_songs(
    session: SessionDep, genre_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get songs by genre.
    """
    genre = crud.get_genre(session=session, genre_id=genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    statement = (
        select(Song)
        .where(Song.genre_id == genre_id)
        .offset(skip)
        .limit(limit)
    )
    songs = list(session.exec(statement))
    count = len(songs)
    return SongsPublic(data=songs, count=count)


@router.get("/{genre_id}/albums", response_model=AlbumsPublic)
def read_genre_albums(
    session: SessionDep, genre_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get albums by genre.
    """
    genre = crud.get_genre(session=session, genre_id=genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    statement = (
        select(Album)
        .where(Album.genre_id == genre_id)
        .where(Album.is_public == True)
        .offset(skip)
        .limit(limit)
    )
    albums = list(session.exec(statement))
    count = len(albums)
    return AlbumsPublic(data=albums, count=count)
