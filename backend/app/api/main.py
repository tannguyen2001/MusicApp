from fastapi import APIRouter

from app.api.routes import login, private, users, utils, social, search, discover, play, files
from app.api.routes.music import (
    artists_router,
    albums_router,
    songs_router,
    playlists_router,
    genres_router
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)

# Music API routes
api_router.include_router(artists_router)
api_router.include_router(albums_router)
api_router.include_router(songs_router)
api_router.include_router(playlists_router)
api_router.include_router(genres_router)

# Social and feature routes
api_router.include_router(social.router)
api_router.include_router(search.router)
api_router.include_router(discover.router)
api_router.include_router(play.router)
api_router.include_router(files.router)

if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
