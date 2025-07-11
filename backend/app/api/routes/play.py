"""
Play history and user activity API routes
"""

import uuid
from typing import Any
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.api.deps import CurrentUser, SessionDep
from app import crud
from app.models import PlayHistory, Message, Song

router = APIRouter(prefix="/play", tags=["play"])


class PlayTrackRequest(BaseModel):
    song_id: uuid.UUID


@router.post("/track", response_model=Message)
def play_track(
    *, session: SessionDep, current_user: CurrentUser, play_data: PlayTrackRequest
) -> Any:
    """
    Record a song play and increment play count.
    """
    # Check if song exists
    song = crud.get_song(session=session, song_id=play_data.song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Increment play count
    crud.increment_play_count(session=session, song_id=play_data.song_id)
    
    # Record play in history (you would implement this in analytics CRUD)
    # For now, just return success
    return Message(message="Play recorded successfully")


@router.get("/history")
def get_play_history(
    *, session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get user's play history.
    """
    # This would use PlayHistory model when implemented
    # For now return empty
    return {"data": [], "count": 0}


@router.get("/recently-played")
def get_recently_played(
    *, session: SessionDep, current_user: CurrentUser, limit: int = 50
) -> Any:
    """
    Get user's recently played songs.
    """
    # This would query PlayHistory table when implemented
    # For now return empty
    return {"data": [], "count": 0}


@router.get("/stats")
def get_user_stats(
    *, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get user's listening statistics.
    """
    # Get user's likes count
    likes_count = len(crud.get_user_likes(session=session, user_id=current_user.id, limit=1000))
    
    # Get user's library count
    library_count = len(crud.get_user_library(session=session, user_id=current_user.id, limit=1000))
    
    # Get user's following count
    following_count = len(crud.get_user_following(session=session, follower_id=current_user.id, limit=1000))
    
    # Get user's followers count
    followers_count = len(crud.get_user_followers(session=session, following_id=current_user.id, limit=1000))
    
    # Get user's playlists count
    playlists_count = len(crud.get_playlists_by_user(session=session, user_id=current_user.id, limit=1000))
    
    return {
        "likes_count": likes_count,
        "library_count": library_count,
        "following_count": following_count,
        "followers_count": followers_count,
        "playlists_count": playlists_count,
        "total_plays": 0,  # Would come from PlayHistory when implemented
        "total_listening_time": 0  # Would be calculated from PlayHistory
    }
