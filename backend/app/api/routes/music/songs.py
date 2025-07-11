"""
Songs API routes
"""

import uuid
from typing import Any
from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse, RedirectResponse
from sqlmodel import select, func

from app.api.deps import CurrentUser, SessionDep
from app import crud
from app.models import (
    Song, SongCreate, SongUpdate, SongPublic, SongsPublic,
    Artist, Album,
    Message,
)

router = APIRouter(prefix="/songs", tags=["songs"])


@router.get("/", response_model=SongsPublic)
def read_songs(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve songs.
    """
    songs = crud.get_songs(session=session, skip=skip, limit=limit)
    count = len(songs)
    return SongsPublic(data=songs, count=count)


@router.get("/{song_id}", response_model=SongPublic)
def read_song(session: SessionDep, song_id: uuid.UUID) -> Any:
    """
    Get song by ID.
    """
    song = crud.get_song(session=session, song_id=song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.post("/", response_model=SongPublic)
def create_song(
    *, session: SessionDep, current_user: CurrentUser, song_in: SongCreate
) -> Any:
    """
    Create new song.
    Only artists can create songs.
    """
    # Check if the album exists
    album = crud.get_album(session=session, album_id=song_in.album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # Check if the artist exists and user owns it
    artist = crud.get_artist(session=session, artist_id=song_in.artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    if artist.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions to create song for this artist"
        )
    
    # Verify that the album belongs to the same artist
    if album.artist_id != song_in.artist_id:
        raise HTTPException(
            status_code=400, 
            detail="Album does not belong to the specified artist"
        )
    
    song = crud.create_song(session=session, song_create=song_in)
    return song


@router.patch("/{song_id}", response_model=SongPublic)
def update_song(
    *, 
    session: SessionDep, 
    current_user: CurrentUser, 
    song_id: uuid.UUID,
    song_in: SongUpdate
) -> Any:
    """
    Update a song.
    Only the artist owner can update their song.
    """
    song = crud.get_song(session=session, song_id=song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Check ownership through artist
    artist = crud.get_artist(session=session, artist_id=song.artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    if artist.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions"
        )
    
    song = crud.update_song(
        session=session, db_song=song, song_in=song_in
    )
    return song


@router.delete("/{song_id}")
def delete_song(
    session: SessionDep, current_user: CurrentUser, song_id: uuid.UUID
) -> Message:
    """
    Delete a song.
    Only the artist owner or superuser can delete.
    """
    song = crud.get_song(session=session, song_id=song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Check ownership through artist
    artist = crud.get_artist(session=session, artist_id=song.artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    if artist.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions"
        )
    
    success = crud.delete_song(session=session, song_id=song_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete song")
    
    return Message(message="Song deleted successfully")


@router.get("/{song_id}/lyrics")
def read_song_lyrics(session: SessionDep, song_id: uuid.UUID) -> Any:
    """
    Get song lyrics.
    """
    song = crud.get_song(session=session, song_id=song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    return {"lyrics": song.lyrics or "No lyrics available"}


@router.post("/{song_id}/play")
async def play_song(
    *, session: SessionDep, current_user: CurrentUser, song_id: uuid.UUID
) -> Message:
    """
    Record a song play and increment play count
    """
    song = crud.get_song(session=session, song_id=song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Increment play count
    crud.increment_play_count(session=session, song_id=song_id)
    
    # TODO: Record in play history when implemented
    
    return Message(message="Play recorded successfully")


@router.get("/trending/", response_model=SongsPublic)
def read_trending_songs(
    session: SessionDep, limit: int = 50
) -> Any:
    """
    Get trending songs (most played recently).
    """
    statement = (
        select(Song)
        .order_by(Song.play_count.desc(), Song.popularity_score.desc())
        .limit(limit)
    )
    songs = list(session.exec(statement))
    count = len(songs)
    return SongsPublic(data=songs, count=count)


@router.get("/search/", response_model=SongsPublic)
def search_songs(
    session: SessionDep, q: str, limit: int = 20
) -> Any:
    """
    Search songs by title.
    """
    statement = (
        select(Song)
        .where(Song.title.ilike(f"%{q}%"))
        .limit(limit)
    )
    songs = list(session.exec(statement))
    count = len(songs)
    return SongsPublic(data=songs, count=count)


@router.get("/{song_id}/stream")
async def stream_song(song_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Stream a song file
    """
    song = crud.get_song(session=session, song_id=song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    if not song.file_url:
        raise HTTPException(status_code=404, detail="Song file not available")
    
    # If it's a local API file URL, redirect to files endpoint
    if song.file_url.startswith("/api/v1/files/songs/"):
        filename = song.file_url.split("/")[-1]
        return RedirectResponse(f"/api/v1/files/songs/{filename}")
    
    # If it's an external URL, redirect directly
    return RedirectResponse(song.file_url)


@router.patch("/{song_id}/lyrics")
def update_song_lyrics(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    song_id: uuid.UUID,
    lyrics: str
) -> Message:
    """
    Update song lyrics (Artist/Admin only)
    """
    song = crud.get_song(session=session, song_id=song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Check permissions
    if not current_user.is_superuser and song.artist_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    song.lyrics = lyrics
    session.add(song)
    session.commit()
    
    return Message(message="Lyrics updated successfully")
