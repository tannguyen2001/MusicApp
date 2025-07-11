"""
User related models
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


# User models
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    username: str | None = Field(default=None, unique=True, max_length=50)
    avatar_url: str | None = Field(default=None)
    date_of_birth: datetime | None = Field(default=None)
    country: str | None = Field(default=None, max_length=2)
    is_premium: bool = Field(default=False)
    is_artist: bool = Field(default=False)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    username: str | None = Field(default=None, max_length=50)
    avatar_url: str | None = Field(default=None)
    date_of_birth: datetime | None = Field(default=None)
    country: str | None = Field(default=None, max_length=2)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    playlists: list["Playlist"] = Relationship(back_populates="owner")
    play_history: list["PlayHistory"] = Relationship(back_populates="user")
    library: list["UserLibrary"] = Relationship(back_populates="user")
    likes: list["Like"] = Relationship(back_populates="user")
    artist_profile: Optional["Artist"] = Relationship(back_populates="user")


class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
