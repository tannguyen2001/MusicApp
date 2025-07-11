"""
Artists API routes
"""

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.api.permissions import check_artist_ownership
from app import crud
from app.models import (
    Artist, ArtistCreate, ArtistUpdate, ArtistPublic, ArtistsPublic,
    Album, AlbumsPublic,
    Song, SongsPublic,
    Message,
)

router = APIRouter(prefix="/artists", tags=["artists"])


@router.get("/", response_model=ArtistsPublic)
def read_artists(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve artists.
    """
    artists = crud.get_artists(session=session, skip=skip, limit=limit)
    count = len(artists)
    return ArtistsPublic(data=artists, count=count)


@router.get("/{artist_id}", response_model=ArtistPublic)
def read_artist(session: SessionDep, artist_id: uuid.UUID) -> Any:
    """
    Get artist by ID.
    """
    artist = crud.get_artist(session=session, artist_id=artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.post("/", response_model=ArtistPublic)
def create_artist(
    *, session: SessionDep, current_user: CurrentUser, artist_in: ArtistCreate
) -> Any:
    """
    Create new artist.
    Only authenticated users can create artist profiles.
    """
    # Check if user already has an artist profile
    existing_artists = crud.get_artists_by_user(session=session, user_id=current_user.id)
    if existing_artists:
        raise HTTPException(
            status_code=400, 
            detail="User already has an artist profile"
        )
    
    artist = crud.create_artist(
        session=session, artist_create=artist_in, user_id=current_user.id
    )
    return artist


@router.patch("/{artist_id}", response_model=ArtistPublic)
def update_artist(
    *, 
    session: SessionDep, 
    current_user: CurrentUser, 
    artist_id: uuid.UUID,
    artist_in: ArtistUpdate
) -> Any:
    """
    Update an artist.
    Only the artist owner can update their profile.
    """
    artist = crud.get_artist(session=session, artist_id=artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    # Check ownership
    if artist.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions"
        )
    
    artist = crud.update_artist(
        session=session, db_artist=artist, artist_in=artist_in
    )
    return artist


@router.delete("/{artist_id}")
def delete_artist(
    session: SessionDep, current_user: CurrentUser, artist_id: uuid.UUID
) -> Message:
    """
    Delete an artist.
    Only the artist owner or superuser can delete.
    """
    artist = crud.get_artist(session=session, artist_id=artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    # Check ownership
    if artist.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions"
        )
    
    success = crud.delete_artist(session=session, artist_id=artist_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete artist")
    
    return Message(message="Artist deleted successfully")


@router.get("/{artist_id}/albums", response_model=AlbumsPublic)
def read_artist_albums(session: SessionDep, artist_id: uuid.UUID) -> Any:
    """
    Get albums by artist.
    """
    artist = crud.get_artist(session=session, artist_id=artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    albums = crud.get_albums_by_artist(session=session, artist_id=artist_id)
    count = len(albums)
    return AlbumsPublic(data=albums, count=count)


@router.get("/{artist_id}/songs", response_model=SongsPublic)
def read_artist_songs(session: SessionDep, artist_id: uuid.UUID) -> Any:
    """
    Get songs by artist.
    """
    artist = crud.get_artist(session=session, artist_id=artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    songs = crud.get_songs_by_artist(session=session, artist_id=artist_id)
    count = len(songs)
    return SongsPublic(data=songs, count=count)


@router.get("/search/", response_model=ArtistsPublic)
def search_artists(
    session: SessionDep, q: str, limit: int = 20
) -> Any:
    """
    Search artists by name.
    """
    statement = (
        select(Artist)
        .where(Artist.stage_name.ilike(f"%{q}%"))
        .limit(limit)
    )
    artists = list(session.exec(statement))
    count = len(artists)
    return ArtistsPublic(data=artists, count=count)
