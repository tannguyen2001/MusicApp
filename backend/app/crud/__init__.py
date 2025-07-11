"""
CRUD operations package for Music App
"""

# Import all CRUD functions for easy access
from .user import *
from .music import *
from .social import *

__all__ = [
    # User CRUD
    "create_user",
    "get_user", 
    "get_user_by_email",
    "get_users",
    "update_user",
    "delete_user",
    "authenticate",
    
    # Music CRUD - Genre
    "create_genre",
    "get_genre",
    "get_genre_by_name",
    "get_genres",
    "update_genre",
    "delete_genre",
    
    # Music CRUD - Artist
    "create_artist",
    "get_artist",
    "get_artist_by_name",
    "get_artists",
    "search_artists",
    "update_artist",
    "delete_artist",
    
    # Music CRUD - Album
    "create_album",
    "get_album",
    "get_albums",
    "get_albums_by_artist",
    "search_albums",
    "update_album",
    "delete_album",
    
    # Music CRUD - Song
    "create_song",
    "get_song",
    "get_songs",
    "get_songs_by_album",
    "get_songs_by_artist",
    "get_songs_by_genre",
    "search_songs",
    "get_popular_songs",
    "increment_play_count",
    "update_song",
    "delete_song",
    
    # Music CRUD - Playlist
    "create_playlist",
    "get_playlist",
    "get_playlists_by_user",
    "get_public_playlists",
    "search_playlists",
    "add_song_to_playlist",
    "remove_song_from_playlist",
    "get_playlist_songs",
    "reorder_playlist_songs",
    "update_playlist",
    "delete_playlist",
    
    # Social CRUD
    "like_item",
    "unlike_item",
    "follow_item", 
    "unfollow_item",
    "save_to_library",
    "remove_from_library",
]
