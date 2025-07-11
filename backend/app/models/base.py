"""
Base models and common schemas
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


# Enums
class AlbumType(str, Enum):
    SINGLE = "single"
    EP = "ep"
    ALBUM = "album"


class TargetType(str, Enum):
    SONG = "song"
    ALBUM = "album"
    PLAYLIST = "playlist"
    ARTIST = "artist"
    USER = "user"


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: Optional[str] = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
