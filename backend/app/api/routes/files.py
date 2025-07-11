"""
File upload and management API routes
"""

import uuid
import os
from typing import Any
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import FileResponse, StreamingResponse

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app import crud
from app.models import Message
from app.core.config import settings

router = APIRouter(prefix="/files", tags=["files"])

# Create upload directories
UPLOAD_DIR = Path("uploads")
SONGS_DIR = UPLOAD_DIR / "songs"
COVERS_DIR = UPLOAD_DIR / "covers"
AVATARS_DIR = UPLOAD_DIR / "avatars"

# Ensure directories exist
for dir_path in [UPLOAD_DIR, SONGS_DIR, COVERS_DIR, AVATARS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


@router.post("/upload/song", response_model=dict)
async def upload_song_file(
    *, 
    session: SessionDep, 
    current_user: CurrentUser,
    file: UploadFile = File(...)
) -> Any:
    """
    Upload a song file (MP3, WAV, FLAC, etc.)
    """
    # Check file type
    allowed_types = ["audio/mpeg", "audio/wav", "audio/flac", "audio/mp4", "audio/ogg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_types)}"
        )
    
    # Check file size (max 50MB)
    max_size = 50 * 1024 * 1024  # 50MB
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > max_size:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 50MB")
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = SONGS_DIR / unique_filename
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Return file info
    file_url = f"/api/v1/files/songs/{unique_filename}"
    
    return {
        "filename": unique_filename,
        "original_filename": file.filename,
        "file_url": file_url,
        "file_path": str(file_path),
        "file_size": file_size,
        "content_type": file.content_type
    }


@router.post("/upload/cover", response_model=dict)
async def upload_cover_image(
    *, 
    session: SessionDep, 
    current_user: CurrentUser,
    file: UploadFile = File(...)
) -> Any:
    """
    Upload album/song cover image
    """
    # Check file type
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_types)}"
        )
    
    # Check file size (max 5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    content = await file.read()
    file_size = len(content)
    
    if file_size > max_size:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 5MB")
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = COVERS_DIR / unique_filename
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Return file info
    file_url = f"/api/v1/files/covers/{unique_filename}"
    
    return {
        "filename": unique_filename,
        "original_filename": file.filename,
        "file_url": file_url,
        "file_path": str(file_path),
        "file_size": file_size,
        "content_type": file.content_type
    }


@router.get("/songs/{filename}")
async def stream_song(filename: str) -> StreamingResponse:
    """
    Stream a song file
    """
    file_path = SONGS_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    def iter_file():
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):  # 8KB chunks
                yield chunk
    
    # Determine content type based on file extension
    content_type = "audio/mpeg"  # Default
    if filename.endswith('.wav'):
        content_type = "audio/wav"
    elif filename.endswith('.flac'):
        content_type = "audio/flac"
    elif filename.endswith('.m4a'):
        content_type = "audio/mp4"
    elif filename.endswith('.ogg'):
        content_type = "audio/ogg"
    
    return StreamingResponse(
        iter_file(),
        media_type=content_type,
        headers={
            "Accept-Ranges": "bytes",
            "Content-Disposition": f"inline; filename={filename}"
        }
    )


@router.get("/covers/{filename}")
async def get_cover_image(filename: str) -> FileResponse:
    """
    Get cover image file
    """
    file_path = COVERS_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        headers={"Cache-Control": "max-age=3600"}  # Cache for 1 hour
    )


@router.delete("/songs/{filename}")
async def delete_song_file(
    *, 
    session: SessionDep, 
    current_user: CurrentUser,
    filename: str
) -> Message:
    """
    Delete a song file (Admin only)
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    file_path = SONGS_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Remove file
    os.remove(file_path)
    
    return Message(message="File deleted successfully")


@router.get("/info/{filename}")
async def get_file_info(filename: str, file_type: str = "song") -> dict:
    """
    Get file information
    """
    if file_type == "song":
        file_path = SONGS_DIR / filename
    elif file_type == "cover":
        file_path = COVERS_DIR / filename
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    stat = file_path.stat()
    
    return {
        "filename": filename,
        "file_size": stat.st_size,
        "created_at": stat.st_ctime,
        "modified_at": stat.st_mtime,
        "file_path": str(file_path)
    }
