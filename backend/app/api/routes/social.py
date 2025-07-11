"""
Social features API routes (Like, Follow, Library)
"""

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app import crud
from app.models import (
    Like, LikeCreate,
    Follow, FollowCreate,
    UserLibrary, UserLibraryCreate,
    Message,
)

router = APIRouter(prefix="/social", tags=["social"])


# ===== LIKE ENDPOINTS =====

@router.post("/like", response_model=Message)
def like_item(
    *, session: SessionDep, current_user: CurrentUser, like_data: LikeCreate
) -> Any:
    """
    Like a song/album/playlist.
    """
    like = crud.like_item(
        session=session,
        user_id=current_user.id,
        target_id=like_data.target_id,
        target_type=like_data.target_type
    )
    return Message(message="Item liked successfully")


@router.delete("/like/{target_id}")
def unlike_item(
    *, session: SessionDep, current_user: CurrentUser, target_id: uuid.UUID, target_type: str
) -> Any:
    """
    Unlike a song/album/playlist.
    """
    success = crud.unlike_item(
        session=session,
        user_id=current_user.id,
        target_id=target_id,
        target_type=target_type
    )
    if not success:
        raise HTTPException(status_code=404, detail="Like not found")
    return Message(message="Item unliked successfully")


@router.get("/like/{target_id}/status")
def check_like_status(
    *, session: SessionDep, current_user: CurrentUser, target_id: uuid.UUID, target_type: str
) -> Any:
    """
    Check if user has liked an item.
    """
    is_liked = crud.is_liked(
        session=session,
        user_id=current_user.id,
        target_id=target_id,
        target_type=target_type
    )
    return {"is_liked": is_liked}


@router.get("/likes")
def get_user_likes(
    *, session: SessionDep, current_user: CurrentUser, target_type: str = None, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get user's likes.
    """
    likes = crud.get_user_likes(
        session=session,
        user_id=current_user.id,
        target_type=target_type,
        skip=skip,
        limit=limit
    )
    return {"data": likes, "count": len(likes)}


# ===== FOLLOW ENDPOINTS =====

@router.post("/follow", response_model=Message)
def follow_item(
    *, session: SessionDep, current_user: CurrentUser, follow_data: FollowCreate
) -> Any:
    """
    Follow an artist/user.
    """
    follow = crud.follow_item(
        session=session,
        follower_id=current_user.id,
        following_id=follow_data.following_id,
        following_type=follow_data.following_type
    )
    return Message(message="Item followed successfully")


@router.delete("/follow/{following_id}")
def unfollow_item(
    *, session: SessionDep, current_user: CurrentUser, following_id: uuid.UUID, following_type: str
) -> Any:
    """
    Unfollow an artist/user.
    """
    success = crud.unfollow_item(
        session=session,
        follower_id=current_user.id,
        following_id=following_id,
        following_type=following_type
    )
    if not success:
        raise HTTPException(status_code=404, detail="Follow not found")
    return Message(message="Item unfollowed successfully")


@router.get("/follow/{following_id}/status")
def check_follow_status(
    *, session: SessionDep, current_user: CurrentUser, following_id: uuid.UUID, following_type: str
) -> Any:
    """
    Check if user is following an item.
    """
    is_following = crud.is_following(
        session=session,
        follower_id=current_user.id,
        following_id=following_id,
        following_type=following_type
    )
    return {"is_following": is_following}


@router.get("/following")
def get_user_following(
    *, session: SessionDep, current_user: CurrentUser, following_type: str = None, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get who user is following.
    """
    following = crud.get_user_following(
        session=session,
        follower_id=current_user.id,
        following_type=following_type,
        skip=skip,
        limit=limit
    )
    return {"data": following, "count": len(following)}


@router.get("/followers")
def get_user_followers(
    *, session: SessionDep, current_user: CurrentUser, following_type: str = None, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get user's followers.
    """
    followers = crud.get_user_followers(
        session=session,
        following_id=current_user.id,
        following_type=following_type,
        skip=skip,
        limit=limit
    )
    return {"data": followers, "count": len(followers)}


# ===== LIBRARY ENDPOINTS =====

@router.post("/library", response_model=Message)
def save_to_library(
    *, session: SessionDep, current_user: CurrentUser, library_data: UserLibraryCreate
) -> Any:
    """
    Save item to user library.
    """
    library_item = crud.save_to_library(
        session=session,
        user_id=current_user.id,
        item_id=library_data.item_id,
        item_type=library_data.item_type
    )
    return Message(message="Item saved to library successfully")


@router.delete("/library/{item_id}")
def remove_from_library(
    *, session: SessionDep, current_user: CurrentUser, item_id: uuid.UUID, item_type: str
) -> Any:
    """
    Remove item from user library.
    """
    success = crud.remove_from_library(
        session=session,
        user_id=current_user.id,
        item_id=item_id,
        item_type=item_type
    )
    if not success:
        raise HTTPException(status_code=404, detail="Item not found in library")
    return Message(message="Item removed from library successfully")


@router.get("/library/{item_id}/status")
def check_library_status(
    *, session: SessionDep, current_user: CurrentUser, item_id: uuid.UUID, item_type: str
) -> Any:
    """
    Check if item is in user's library.
    """
    is_in_library = crud.is_in_library(
        session=session,
        user_id=current_user.id,
        item_id=item_id,
        item_type=item_type
    )
    return {"is_in_library": is_in_library}


@router.get("/library")
def get_user_library(
    *, session: SessionDep, current_user: CurrentUser, item_type: str = None, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get user's library items.
    """
    library_items = crud.get_user_library(
        session=session,
        user_id=current_user.id,
        item_type=item_type,
        skip=skip,
        limit=limit
    )
    return {"data": library_items, "count": len(library_items)}
