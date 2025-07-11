"""
Models package for Music App
"""

# Import all models for SQLModel to detect them
from .base import *
from .user import *
from .music import *
from .social import *
from .analytics import *

__all__ = [
    # Base models
    "Message",
    "Token",
    "TokenPayload", 
    "NewPassword",
    
    # User models
    "User",
    "UserBase",
    "UserCreate",
    "UserRegister", 
    "UserUpdate",
    "UserUpdateMe",
    "UpdatePassword",
    "UserPublic",
    "UsersPublic",
    
    # Music models
    "Genre",
    "GenreBase",
    "GenreCreate", 
    "GenreUpdate",
    "GenrePublic",
    "GenresPublic",
    "Artist",
    "ArtistBase",
    "ArtistCreate",
    "ArtistUpdate", 
    "ArtistPublic",
    "ArtistsPublic",
    "Album", 
    "AlbumBase",
    "AlbumCreate",
    "AlbumUpdate",
    "AlbumPublic",
    "AlbumsPublic",
    "Song",
    "SongBase", 
    "SongCreate",
    "SongUpdate",
    "SongPublic",
    "SongsPublic",
    "Playlist",
    "PlaylistBase",
    "PlaylistCreate",
    "PlaylistUpdate", 
    "PlaylistPublic",
    "PlaylistsPublic",
    "PlaylistSong",
    
    # Social models
    "Follow",
    "FollowCreate",
    "Like",
    "LikeCreate", 
    "UserLibrary",
    "UserLibraryCreate",
    
    # Analytics models
    "PlayHistory",
    "SearchHistory", 
    "Recommendation",
    
    # Enums
    "AlbumType",
    "TargetType",
]
