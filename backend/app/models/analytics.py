"""
Analytics and tracking models (PlayHistory, SearchHistory, Recommendations)
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from .base import TargetType


# Play History
class PlayHistory(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    song_id: uuid.UUID = Field(foreign_key="song.id")
    played_at: datetime = Field(default_factory=datetime.utcnow)
    duration_played_ms: int
    device_type: str | None = Field(default=None)
    skip_reason: str | None = Field(default=None)
    
    # Relationships
    user: "User" = Relationship(back_populates="play_history")


# Search History
class SearchHistory(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    query: str = Field(max_length=255)
    result_type: TargetType | None = Field(default=None)
    result_id: uuid.UUID | None = Field(default=None)
    searched_at: datetime = Field(default_factory=datetime.utcnow)


# Recommendations
class Recommendation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    song_id: uuid.UUID = Field(foreign_key="song.id")
    recommendation_type: str = Field(max_length=100)  # daily_mix, discover_weekly, etc.
    score: float = Field(ge=0.0, le=1.0)
    reason: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
