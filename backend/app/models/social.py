"""
Social features models (Follow, Like, UserLibrary)
"""

import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from .base import TargetType

if TYPE_CHECKING:
    from .user import User


# Follow System
class FollowBase(SQLModel):
    following_id: uuid.UUID
    following_type: TargetType


class Follow(FollowBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    follower_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FollowCreate(FollowBase):
    pass


# Like System
class LikeBase(SQLModel):
    target_id: uuid.UUID
    target_type: TargetType


class Like(LikeBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship(back_populates="likes")


class LikeCreate(LikeBase):
    pass


# User Library (Saved items)
class UserLibraryBase(SQLModel):
    item_id: uuid.UUID
    item_type: TargetType


class UserLibrary(UserLibraryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    saved_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship(back_populates="library")


class UserLibraryCreate(UserLibraryBase):
    pass
