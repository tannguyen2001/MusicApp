"""
Social features CRUD operations (Like, Follow, UserLibrary)
"""

import uuid
from typing import Any

from sqlmodel import Session, select

from app.models import Like, Follow, UserLibrary


def like_item(
    *, session: Session, user_id: uuid.UUID, target_id: uuid.UUID, target_type: str
) -> Like:
    """Like a song/album/playlist"""
    # Check if already liked
    statement = select(Like).where(
        Like.user_id == user_id,
        Like.target_id == target_id,
        Like.target_type == target_type
    )
    existing = session.exec(statement).first()
    if existing:
        return existing
    
    db_obj = Like(
        user_id=user_id,
        target_id=target_id,
        target_type=target_type
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def unlike_item(
    *, session: Session, user_id: uuid.UUID, target_id: uuid.UUID, target_type: str
) -> bool:
    """Unlike a song/album/playlist"""
    statement = select(Like).where(
        Like.user_id == user_id,
        Like.target_id == target_id,
        Like.target_type == target_type
    )
    like = session.exec(statement).first()
    if like:
        session.delete(like)
        session.commit()
        return True
    return False


def is_liked(
    *, session: Session, user_id: uuid.UUID, target_id: uuid.UUID, target_type: str
) -> bool:
    """Check if user has liked an item"""
    statement = select(Like).where(
        Like.user_id == user_id,
        Like.target_id == target_id,
        Like.target_type == target_type
    )
    return session.exec(statement).first() is not None


def get_user_likes(
    *, session: Session, user_id: uuid.UUID, target_type: str = None, skip: int = 0, limit: int = 100
) -> list[Like]:
    """Get user's likes, optionally filtered by type"""
    statement = select(Like).where(Like.user_id == user_id)
    if target_type:
        statement = statement.where(Like.target_type == target_type)
    statement = statement.offset(skip).limit(limit).order_by(Like.created_at.desc())
    return list(session.exec(statement))


def follow_item(
    *, session: Session, follower_id: uuid.UUID, following_id: uuid.UUID, following_type: str
) -> Follow:
    """Follow an artist/user"""
    # Check if already following
    statement = select(Follow).where(
        Follow.follower_id == follower_id,
        Follow.following_id == following_id,
        Follow.following_type == following_type
    )
    existing = session.exec(statement).first()
    if existing:
        return existing
    
    db_obj = Follow(
        follower_id=follower_id,
        following_id=following_id,
        following_type=following_type
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def unfollow_item(
    *, session: Session, follower_id: uuid.UUID, following_id: uuid.UUID, following_type: str
) -> bool:
    """Unfollow an artist/user"""
    statement = select(Follow).where(
        Follow.follower_id == follower_id,
        Follow.following_id == following_id,
        Follow.following_type == following_type
    )
    follow = session.exec(statement).first()
    if follow:
        session.delete(follow)
        session.commit()
        return True
    return False


def is_following(
    *, session: Session, follower_id: uuid.UUID, following_id: uuid.UUID, following_type: str
) -> bool:
    """Check if user is following an item"""
    statement = select(Follow).where(
        Follow.follower_id == follower_id,
        Follow.following_id == following_id,
        Follow.following_type == following_type
    )
    return session.exec(statement).first() is not None


def get_user_following(
    *, session: Session, follower_id: uuid.UUID, following_type: str = None, skip: int = 0, limit: int = 100
) -> list[Follow]:
    """Get who user is following"""
    statement = select(Follow).where(Follow.follower_id == follower_id)
    if following_type:
        statement = statement.where(Follow.following_type == following_type)
    statement = statement.offset(skip).limit(limit).order_by(Follow.created_at.desc())
    return list(session.exec(statement))


def get_user_followers(
    *, session: Session, following_id: uuid.UUID, following_type: str = None, skip: int = 0, limit: int = 100
) -> list[Follow]:
    """Get user's followers"""
    statement = select(Follow).where(Follow.following_id == following_id)
    if following_type:
        statement = statement.where(Follow.following_type == following_type)
    statement = statement.offset(skip).limit(limit).order_by(Follow.created_at.desc())
    return list(session.exec(statement))


def save_to_library(
    *, session: Session, user_id: uuid.UUID, item_id: uuid.UUID, item_type: str
) -> UserLibrary:
    """Save item to user library"""
    # Check if already saved
    statement = select(UserLibrary).where(
        UserLibrary.user_id == user_id,
        UserLibrary.item_id == item_id,
        UserLibrary.item_type == item_type
    )
    existing = session.exec(statement).first()
    if existing:
        return existing
    
    db_obj = UserLibrary(
        user_id=user_id,
        item_id=item_id,
        item_type=item_type
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def remove_from_library(
    *, session: Session, user_id: uuid.UUID, item_id: uuid.UUID, item_type: str
) -> bool:
    """Remove item from user library"""
    statement = select(UserLibrary).where(
        UserLibrary.user_id == user_id,
        UserLibrary.item_id == item_id,
        UserLibrary.item_type == item_type
    )
    library_item = session.exec(statement).first()
    if library_item:
        session.delete(library_item)
        session.commit()
        return True
    return False


def is_in_library(
    *, session: Session, user_id: uuid.UUID, item_id: uuid.UUID, item_type: str
) -> bool:
    """Check if item is in user's library"""
    statement = select(UserLibrary).where(
        UserLibrary.user_id == user_id,
        UserLibrary.item_id == item_id,
        UserLibrary.item_type == item_type
    )
    return session.exec(statement).first() is not None


def get_user_library(
    *, session: Session, user_id: uuid.UUID, item_type: str = None, skip: int = 0, limit: int = 100
) -> list[UserLibrary]:
    """Get user's library items"""
    statement = select(UserLibrary).where(UserLibrary.user_id == user_id)
    if item_type:
        statement = statement.where(UserLibrary.item_type == item_type)
    statement = statement.offset(skip).limit(limit).order_by(UserLibrary.saved_at.desc())
    return list(session.exec(statement))
