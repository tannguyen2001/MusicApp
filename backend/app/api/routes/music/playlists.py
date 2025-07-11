"""
Playlists API routes
"""

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app import crud
from app.models import (
    Playlist, PlaylistCreate, PlaylistUpdate, PlaylistPublic, PlaylistsPublic,
    Song, SongsPublic,
    Message,
)

router = APIRouter(prefix="/playlists", tags=["playlists"])


@router.get("/", response_model=PlaylistsPublic)
def read_playlists(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve public playlists.
    """
    playlists = crud.get_playlists(session=session, skip=skip, limit=limit)
    count = len(playlists)
    return PlaylistsPublic(data=playlists, count=count)


@router.get("/{playlist_id}", response_model=PlaylistPublic)
def read_playlist(session: SessionDep, playlist_id: uuid.UUID) -> Any:
    """
    Get playlist by ID.
    """
    playlist = crud.get_playlist(session=session, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


@router.post("/", response_model=PlaylistPublic)
def create_playlist(
    *, session: SessionDep, current_user: CurrentUser, playlist_in: PlaylistCreate
) -> Any:
    """
    Create new playlist.
    """
    playlist = crud.create_playlist(
        session=session, playlist_create=playlist_in, owner_id=current_user.id
    )
    return playlist


@router.patch("/{playlist_id}", response_model=PlaylistPublic)
def update_playlist(
    *, 
    session: SessionDep, 
    current_user: CurrentUser, 
    playlist_id: uuid.UUID,
    playlist_in: PlaylistUpdate
) -> Any:
    """
    Update a playlist.
    Only the playlist owner can update their playlist.
    """
    playlist = crud.get_playlist(session=session, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Check ownership
    if playlist.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions"
        )
    
    playlist = crud.update_playlist(
        session=session, db_playlist=playlist, playlist_in=playlist_in
    )
    return playlist


@router.delete("/{playlist_id}")
def delete_playlist(
    session: SessionDep, current_user: CurrentUser, playlist_id: uuid.UUID
) -> Message:
    """
    Delete a playlist.
    Only the playlist owner or superuser can delete.
    """
    playlist = crud.get_playlist(session=session, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Check ownership
    if playlist.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions"
        )
    
    success = crud.delete_playlist(session=session, playlist_id=playlist_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete playlist")
    
    return Message(message="Playlist deleted successfully")


@router.get("/{playlist_id}/songs", response_model=SongsPublic)
def read_playlist_songs(session: SessionDep, playlist_id: uuid.UUID) -> Any:
    """
    Get songs in playlist (ordered by position).
    """
    playlist = crud.get_playlist(session=session, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    songs = crud.get_playlist_songs(session=session, playlist_id=playlist_id)
    count = len(songs)
    return SongsPublic(data=songs, count=count)


@router.post("/{playlist_id}/songs/{song_id}")
def add_song_to_playlist(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    playlist_id: uuid.UUID,
    song_id: uuid.UUID,
    position: int = None
) -> Message:
    """
    Add song to playlist.
    Only playlist owner or collaborators can add songs.
    """
    playlist = crud.get_playlist(session=session, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Check permissions
    if playlist.owner_id != current_user.id and not playlist.is_collaborative:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions to add songs to this playlist"
        )
    
    # Check if song exists
    song = crud.get_song(session=session, song_id=song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    crud.add_song_to_playlist(
        session=session,
        playlist_id=playlist_id,
        song_id=song_id,
        user_id=current_user.id,
        position=position
    )
    
    return Message(message="Song added to playlist successfully")


@router.delete("/{playlist_id}/songs/{song_id}")
def remove_song_from_playlist(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    playlist_id: uuid.UUID,
    song_id: uuid.UUID
) -> Message:
    """
    Remove song from playlist.
    Only playlist owner can remove songs.
    """
    playlist = crud.get_playlist(session=session, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Check ownership
    if playlist.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions"
        )
    
    success = crud.remove_song_from_playlist(
        session=session, playlist_id=playlist_id, song_id=song_id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Song not found in playlist")
    
    return Message(message="Song removed from playlist successfully")


@router.post("/{playlist_id}/follow")
def follow_playlist(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    playlist_id: uuid.UUID
) -> Message:
    """
    Follow a public playlist.
    """
    playlist = crud.get_playlist(session=session, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    if not playlist.is_public:
        raise HTTPException(status_code=403, detail="Cannot follow private playlist")
    
    crud.follow_item(
        session=session,
        follower_id=current_user.id,
        following_id=playlist_id,
        following_type="playlist"
    )
    
    return Message(message="Playlist followed successfully")


@router.delete("/{playlist_id}/follow")
def unfollow_playlist(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    playlist_id: uuid.UUID
) -> Message:
    """
    Unfollow a playlist.
    """
    success = crud.unfollow_item(
        session=session,
        follower_id=current_user.id,
        following_id=playlist_id,
        following_type="playlist"
    )
    if not success:
        raise HTTPException(status_code=404, detail="Not following this playlist")
    
    return Message(message="Playlist unfollowed successfully")


@router.get("/search/", response_model=PlaylistsPublic)
def search_playlists(
    session: SessionDep, q: str, limit: int = 20
) -> Any:
    """
    Search public playlists by name.
    """
    statement = (
        select(Playlist)
        .where(Playlist.name.ilike(f"%{q}%"))
        .where(Playlist.is_public == True)
        .limit(limit)
    )
    playlists = list(session.exec(statement))
    count = len(playlists)
    return PlaylistsPublic(data=playlists, count=count)
