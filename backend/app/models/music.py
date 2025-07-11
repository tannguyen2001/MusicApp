"""
Music related models (Genre, Artist, Album, Song, Playlist)
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

from .base import AlbumType

if TYPE_CHECKING:
    from .user import User


# Genre models
class GenreBase(SQLModel):
    name: str = Field(unique=True, max_length=100)
    description: Optional[str] = Field(default=None)
    color_code: Optional[str] = Field(default=None, max_length=7)


class Genre(GenreBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    parent_genre_id: Optional[uuid.UUID] = Field(default=None, foreign_key="genre.id")
    
    # Relationships
    albums: list["Album"] = Relationship(back_populates="genre")
    songs: list["Song"] = Relationship(back_populates="genre")


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    name: Optional[str] = None
    description: Optional[str] = None
    color_code: Optional[str] = None


class GenrePublic(GenreBase):
    id: uuid.UUID


class GenresPublic(SQLModel):
    data: list[GenrePublic]
    count: int


# Artist models
class ArtistBase(SQLModel):
    stage_name: str = Field(unique=True, max_length=255)
    biography: Optional[str] = Field(default=None, max_length=2000)
    avatar_url: Optional[str] = Field(default=None)
    banner_url: Optional[str] = Field(default=None)
    verified: bool = Field(default=False)
    followers_count: int = Field(default=0)
    monthly_listeners: int = Field(default=0)


class Artist(ArtistBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional["User"] = Relationship(back_populates="artist_profile")
    albums: list["Album"] = Relationship(back_populates="artist")
    songs: list["Song"] = Relationship(back_populates="artist")


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(ArtistBase):
    stage_name: str | None = Field(default=None, max_length=255)


class ArtistPublic(ArtistBase):
    id: uuid.UUID
    created_at: datetime


class ArtistsPublic(SQLModel):
    data: list[ArtistPublic]
    count: int


# Album models
class AlbumBase(SQLModel):
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    cover_image_url: str | None = Field(default=None)
    release_date: datetime | None = Field(default=None)
    album_type: AlbumType = Field(default=AlbumType.ALBUM)
    total_tracks: int = Field(default=0)
    duration_ms: int = Field(default=0)
    label: str | None = Field(default=None, max_length=255)
    is_public: bool = Field(default=True)


class Album(AlbumBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    artist_id: uuid.UUID = Field(foreign_key="artist.id")
    genre_id: uuid.UUID | None = Field(default=None, foreign_key="genre.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    artist: Artist = Relationship(back_populates="albums")
    genre: Optional[Genre] = Relationship(back_populates="albums")
    songs: list["Song"] = Relationship(back_populates="album")


class AlbumCreate(AlbumBase):
    artist_id: uuid.UUID


class AlbumUpdate(AlbumBase):
    title: str | None = Field(default=None, max_length=255)


class AlbumPublic(AlbumBase):
    id: uuid.UUID
    artist_id: uuid.UUID
    created_at: datetime


class AlbumsPublic(SQLModel):
    data: list[AlbumPublic]
    count: int


# Song models
class SongBase(SQLModel):
    title: str = Field(max_length=255)
    duration_ms: int
    track_number: int = Field(default=1)
    disc_number: int = Field(default=1)
    file_url: str | None = Field(default=None)
    preview_url: str | None = Field(default=None)
    lyrics: str | None = Field(default=None)
    explicit: bool = Field(default=False)
    popularity_score: float = Field(default=0.0, ge=0.0, le=100.0)
    play_count: int = Field(default=0)


class Song(SongBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    album_id: uuid.UUID = Field(foreign_key="album.id")
    artist_id: uuid.UUID = Field(foreign_key="artist.id")
    genre_id: uuid.UUID | None = Field(default=None, foreign_key="genre.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    album: Album = Relationship(back_populates="songs")
    artist: Artist = Relationship(back_populates="songs")
    genre: Optional[Genre] = Relationship(back_populates="songs")
    playlist_songs: list["PlaylistSong"] = Relationship(back_populates="song")


class SongCreate(SongBase):
    album_id: uuid.UUID
    artist_id: uuid.UUID


class SongUpdate(SongBase):
    title: str | None = Field(default=None, max_length=255)
    duration_ms: int | None = Field(default=None)


class SongPublic(SongBase):
    id: uuid.UUID
    album_id: uuid.UUID
    artist_id: uuid.UUID
    created_at: datetime


class SongsPublic(SQLModel):
    data: list[SongPublic]
    count: int


# Playlist models
class PlaylistBase(SQLModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    cover_image_url: str | None = Field(default=None)
    is_public: bool = Field(default=True)
    is_collaborative: bool = Field(default=False)
    follower_count: int = Field(default=0)
    total_tracks: int = Field(default=0)
    total_duration_ms: int = Field(default=0)


class Playlist(PlaylistBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    owner: "User" = Relationship(back_populates="playlists")
    playlist_songs: list["PlaylistSong"] = Relationship(back_populates="playlist")


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistUpdate(PlaylistBase):
    name: str | None = Field(default=None, max_length=255)


class PlaylistPublic(PlaylistBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PlaylistsPublic(SQLModel):
    data: list[PlaylistPublic]
    count: int


# Many-to-Many: Playlist Songs
class PlaylistSong(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    playlist_id: uuid.UUID = Field(foreign_key="playlist.id")
    song_id: uuid.UUID = Field(foreign_key="song.id")
    position: int
    added_by: uuid.UUID = Field(foreign_key="user.id")
    added_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    playlist: Playlist = Relationship(back_populates="playlist_songs")
    song: Song = Relationship(back_populates="playlist_songs")
