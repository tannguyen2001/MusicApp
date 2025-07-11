"""
Permission dependencies for API routes
"""

from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session

from app.api.deps import CurrentUser, SessionDep
from app import crud
from app.models import Artist, Album, Song, Playlist
import uuid


def get_current_active_superuser_or_artist(
    current_user: CurrentUser,
) -> CurrentUser:
    """
    Check if user is superuser or verified artist
    """
    if not current_user.is_superuser and not getattr(current_user, 'artist_profile', None):
        raise HTTPException(
            status_code=403, 
            detail="Only superusers or verified artists can perform this action"
        )
    return current_user


def check_artist_ownership(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    artist_id: uuid.UUID
) -> Artist:
    """
    Check if current user owns the artist profile or is superuser
    """
    artist = crud.get_artist(session=session, artist_id=artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    # Superuser can access any artist
    if current_user.is_superuser:
        return artist
    
    # Check if user owns this artist profile
    if not hasattr(current_user, 'artist_profile') or current_user.artist_profile.id != artist_id:
        raise HTTPException(
            status_code=403, 
            detail="You can only manage your own artist profile"
        )
    
    return artist


def check_album_ownership(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    album_id: uuid.UUID
) -> Album:
    """
    Check if current user owns the album or is superuser
    """
    album = crud.get_album(session=session, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # Superuser can access any album
    if current_user.is_superuser:
        return album
    
    # Check if user owns this album
    if not hasattr(current_user, 'artist_profile') or album.artist_id != current_user.artist_profile.id:
        raise HTTPException(
            status_code=403, 
            detail="You can only manage your own albums"
        )
    
    return album


def check_song_ownership(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    song_id: uuid.UUID
) -> Song:
    """
    Check if current user owns the song or is superuser
    """
    song = crud.get_song(session=session, song_id=song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Superuser can access any song
    if current_user.is_superuser:
        return song
    
    # Check if user owns this song
    if not hasattr(current_user, 'artist_profile') or song.artist_id != current_user.artist_profile.id:
        raise HTTPException(
            status_code=403, 
            detail="You can only manage your own songs"
        )
    
    return song


def check_playlist_ownership(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    playlist_id: uuid.UUID
) -> Playlist:
    """
    Check if current user owns the playlist or is superuser
    """
    playlist = crud.get_playlist(session=session, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Superuser can access any playlist
    if current_user.is_superuser:
        return playlist
    
    # Check if user owns this playlist
    if playlist.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You can only manage your own playlists"
        )
    
    return playlist


# Type annotations for dependencies
CurrentSuperuserOrArtist = Annotated[CurrentUser, Depends(get_current_active_superuser_or_artist)]
ArtistOwnership = Annotated[Artist, Depends(check_artist_ownership)]
AlbumOwnership = Annotated[Album, Depends(check_album_ownership)]
SongOwnership = Annotated[Song, Depends(check_song_ownership)]
PlaylistOwnership = Annotated[Playlist, Depends(check_playlist_ownership)]
