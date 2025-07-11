"""
Albums API routes
"""

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app import crud
from app.models import (
    Album, AlbumCreate, AlbumUpdate, AlbumPublic, AlbumsPublic,
    Song, SongsPublic,
    Artist,
    Message,
)

router = APIRouter(prefix="/albums", tags=["albums"])


@router.get("/", response_model=AlbumsPublic)
def read_albums(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve albums.
    """
    albums = crud.get_albums(session=session, skip=skip, limit=limit)
    count = len(albums)
    return AlbumsPublic(data=albums, count=count)


@router.get("/{album_id}", response_model=AlbumPublic)
def read_album(session: SessionDep, album_id: uuid.UUID) -> Any:
    """
    Get album by ID.
    """
    album = crud.get_album(session=session, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album


@router.post("/", response_model=AlbumPublic)
def create_album(
    *, session: SessionDep, current_user: CurrentUser, album_in: AlbumCreate
) -> Any:
    """
    Create new album.
    Only artists can create albums.
    """
    # Check if the artist exists and user owns it
    artist = crud.get_artist(session=session, artist_id=album_in.artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    if artist.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions to create album for this artist"
        )
    
    album = crud.create_album(session=session, album_create=album_in)
    return album


@router.patch("/{album_id}", response_model=AlbumPublic)
def update_album(
    *, 
    session: SessionDep, 
    current_user: CurrentUser, 
    album_id: uuid.UUID,
    album_in: AlbumUpdate
) -> Any:
    """
    Update an album.
    Only the artist owner can update their album.
    """
    album = crud.get_album(session=session, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # Check ownership through artist
    artist = crud.get_artist(session=session, artist_id=album.artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    if artist.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions"
        )
    
    album = crud.update_album(
        session=session, db_album=album, album_in=album_in
    )
    return album


@router.delete("/{album_id}")
def delete_album(
    session: SessionDep, current_user: CurrentUser, album_id: uuid.UUID
) -> Message:
    """
    Delete an album.
    Only the artist owner or superuser can delete.
    """
    album = crud.get_album(session=session, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # Check ownership through artist
    artist = crud.get_artist(session=session, artist_id=album.artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    if artist.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions"
        )
    
    success = crud.delete_album(session=session, album_id=album_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete album")
    
    return Message(message="Album deleted successfully")


@router.get("/{album_id}/songs", response_model=SongsPublic)
def read_album_songs(session: SessionDep, album_id: uuid.UUID) -> Any:
    """
    Get songs in album (ordered by track number).
    """
    album = crud.get_album(session=session, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    songs = crud.get_songs_by_album(session=session, album_id=album_id)
    count = len(songs)
    return SongsPublic(data=songs, count=count)


@router.get("/new-releases/", response_model=AlbumsPublic)
def read_new_releases(
    session: SessionDep, limit: int = 20
) -> Any:
    """
    Get new releases (albums released recently).
    """
    statement = (
        select(Album)
        .where(Album.is_public == True)
        .order_by(Album.release_date.desc())
        .limit(limit)
    )
    albums = list(session.exec(statement))
    count = len(albums)
    return AlbumsPublic(data=albums, count=count)


@router.get("/search/", response_model=AlbumsPublic)
def search_albums(
    session: SessionDep, q: str, limit: int = 20
) -> Any:
    """
    Search albums by title.
    """
    statement = (
        select(Album)
        .where(Album.title.ilike(f"%{q}%"))
        .where(Album.is_public == True)
        .limit(limit)
    )
    albums = list(session.exec(statement))
    count = len(albums)
    return AlbumsPublic(data=albums, count=count)
