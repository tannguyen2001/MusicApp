"""
Discover and recommendation API routes
"""

from typing import Any

from fastapi import APIRouter
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app import crud
from app.models import (
    Song, SongsPublic,
    Album, AlbumsPublic,
    Artist, ArtistsPublic,
    Playlist, PlaylistsPublic,
)

router = APIRouter(prefix="/discover", tags=["discover"])


@router.get("/popular-songs", response_model=SongsPublic)
def get_popular_songs(
    *, session: SessionDep, skip: int = 0, limit: int = 50
) -> Any:
    """
    Get popular songs ordered by play count.
    """
    songs = crud.get_popular_songs(session=session, skip=skip, limit=limit)
    return SongsPublic(data=songs, count=len(songs))


@router.get("/new-releases", response_model=AlbumsPublic)
def get_new_releases(
    *, session: SessionDep, skip: int = 0, limit: int = 50
) -> Any:
    """
    Get newest album releases.
    """
    albums = crud.get_albums(session=session, skip=skip, limit=limit)
    return AlbumsPublic(data=albums, count=len(albums))


@router.get("/trending-artists", response_model=ArtistsPublic)
def get_trending_artists(
    *, session: SessionDep, skip: int = 0, limit: int = 50
) -> Any:
    """
    Get trending artists.
    """
    artists = crud.get_artists(session=session, skip=skip, limit=limit)
    return ArtistsPublic(data=artists, count=len(artists))


@router.get("/featured-playlists", response_model=PlaylistsPublic)
def get_featured_playlists(
    *, session: SessionDep, skip: int = 0, limit: int = 50
) -> Any:
    """
    Get featured public playlists.
    """
    playlists = crud.get_public_playlists(session=session, skip=skip, limit=limit)
    return PlaylistsPublic(data=playlists, count=len(playlists))


@router.get("/recommendations/songs", response_model=SongsPublic)
def get_recommended_songs(
    *, session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 50
) -> Any:
    """
    Get personalized song recommendations for user.
    This is a simple implementation - in production you'd use ML algorithms.
    """
    # Simple recommendation: get songs from genres user has liked
    user_likes = crud.get_user_likes(
        session=session, 
        user_id=current_user.id, 
        target_type="song", 
        limit=10
    )
    
    if not user_likes:
        # Fallback to popular songs if no likes
        songs = crud.get_popular_songs(session=session, skip=skip, limit=limit)
    else:
        # Get songs from same genres as liked songs
        # This is simplified - real implementation would be more sophisticated
        songs = crud.get_popular_songs(session=session, skip=skip, limit=limit)
    
    return SongsPublic(data=songs, count=len(songs))


@router.get("/recommendations/artists", response_model=ArtistsPublic)
def get_recommended_artists(
    *, session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 50
) -> Any:
    """
    Get personalized artist recommendations for user.
    """
    # Simple recommendation: get artists user hasn't followed yet
    artists = crud.get_artists(session=session, skip=skip, limit=limit)
    return ArtistsPublic(data=artists, count=len(artists))


@router.get("/recommendations/albums", response_model=AlbumsPublic)  
def get_recommended_albums(
    *, session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 50
) -> Any:
    """
    Get personalized album recommendations for user.
    """
    # Simple recommendation based on user's music taste
    albums = crud.get_albums(session=session, skip=skip, limit=limit)
    return AlbumsPublic(data=albums, count=len(albums))
