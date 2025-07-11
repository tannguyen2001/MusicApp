"""
Music API routes package
"""

from .artists import router as artists_router
from .albums import router as albums_router  
from .songs import router as songs_router
from .playlists import router as playlists_router
from .genres import router as genres_router

__all__ = [
    "artists_router",
    "albums_router", 
    "songs_router",
    "playlists_router",
    "genres_router"
]
