"""
Search API routes
"""

from typing import Any

from fastapi import APIRouter, Query
from sqlmodel import select

from app.api.deps import SessionDep
from app import crud
from app.models import (
    Artist, ArtistsPublic,
    Album, AlbumsPublic,
    Song, SongsPublic,
    Playlist, PlaylistsPublic,
)

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/all")
def search_all(
    *, session: SessionDep, q: str = Query(..., min_length=1, description="Search query")
) -> Any:
    """
    Search across all content types.
    """
    # Search artists
    artists = crud.search_artists(session=session, query=q, limit=10)
    
    # Search albums
    albums = crud.search_albums(session=session, query=q, limit=10)
    
    # Search songs
    songs = crud.search_songs(session=session, query=q, limit=10)
    
    # Search playlists
    playlists = crud.search_playlists(session=session, query=q, limit=10)
    
    return {
        "artists": {"data": artists, "count": len(artists)},
        "albums": {"data": albums, "count": len(albums)},
        "songs": {"data": songs, "count": len(songs)},
        "playlists": {"data": playlists, "count": len(playlists)}
    }


@router.get("/artists", response_model=ArtistsPublic)
def search_artists(
    *, session: SessionDep, q: str = Query(..., min_length=1), skip: int = 0, limit: int = 50
) -> Any:
    """
    Search artists.
    """
    artists = crud.search_artists(session=session, query=q, skip=skip, limit=limit)
    return ArtistsPublic(data=artists, count=len(artists))


@router.get("/albums", response_model=AlbumsPublic)
def search_albums(
    *, session: SessionDep, q: str = Query(..., min_length=1), skip: int = 0, limit: int = 50
) -> Any:
    """
    Search albums.
    """
    albums = crud.search_albums(session=session, query=q, skip=skip, limit=limit)
    return AlbumsPublic(data=albums, count=len(albums))


@router.get("/songs", response_model=SongsPublic)
def search_songs(
    *, session: SessionDep, q: str = Query(..., min_length=1), skip: int = 0, limit: int = 50
) -> Any:
    """
    Search songs.
    """
    songs = crud.search_songs(session=session, query=q, skip=skip, limit=limit)
    return SongsPublic(data=songs, count=len(songs))


@router.get("/playlists", response_model=PlaylistsPublic)
def search_playlists(
    *, session: SessionDep, q: str = Query(..., min_length=1), skip: int = 0, limit: int = 50
) -> Any:
    """
    Search public playlists.
    """
    playlists = crud.search_playlists(session=session, query=q, skip=skip, limit=limit)
    return PlaylistsPublic(data=playlists, count=len(playlists))
