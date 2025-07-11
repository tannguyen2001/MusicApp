"""
CRUD operations for music domain
"""
from typing import Any
from uuid import UUID
from sqlmodel import Session, select, func, and_, or_, desc, asc

from app.models.music import (
    Genre, GenreCreate, GenreUpdate,
    Artist, ArtistCreate, ArtistUpdate,
    Album, AlbumCreate, AlbumUpdate,
    Song, SongCreate, SongUpdate,
    Playlist, PlaylistCreate, PlaylistUpdate,
    PlaylistSong,
)
from app.models.user import User


# ===== GENRE CRUD =====

def create_genre(*, session: Session, genre_create: GenreCreate) -> Genre:
    """Create a new genre"""
    db_obj = Genre.model_validate(genre_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_genre(*, session: Session, genre_id: UUID) -> Genre | None:
    """Get genre by ID"""
    return session.get(Genre, genre_id)


def get_genre_by_name(*, session: Session, name: str) -> Genre | None:
    """Get genre by name"""
    statement = select(Genre).where(Genre.name == name)
    return session.exec(statement).first()


def get_genres(
    *, session: Session, skip: int = 0, limit: int = 100
) -> list[Genre]:
    """Get all genres with pagination"""
    statement = select(Genre).offset(skip).limit(limit).order_by(Genre.name)
    return session.exec(statement).all()


def update_genre(
    *, session: Session, db_genre: Genre, genre_update: GenreUpdate
) -> Genre:
    """Update a genre"""
    genre_data = genre_update.model_dump(exclude_unset=True)
    db_genre.sqlmodel_update(genre_data)
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre


def delete_genre(*, session: Session, genre_id: UUID) -> bool:
    """Delete a genre"""
    genre = session.get(Genre, genre_id)
    if genre:
        session.delete(genre)
        session.commit()
        return True
    return False


# ===== ARTIST CRUD =====

def create_artist(*, session: Session, artist_create: ArtistCreate) -> Artist:
    """Create a new artist"""
    db_obj = Artist.model_validate(artist_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_artist(*, session: Session, artist_id: UUID) -> Artist | None:
    """Get artist by ID"""
    return session.get(Artist, artist_id)


def get_artist_by_name(*, session: Session, name: str) -> Artist | None:
    """Get artist by name"""
    statement = select(Artist).where(Artist.name == name)
    return session.exec(statement).first()


def get_artists(
    *, session: Session, skip: int = 0, limit: int = 100
) -> list[Artist]:
    """Get all artists with pagination"""
    statement = select(Artist).offset(skip).limit(limit).order_by(Artist.name)
    return session.exec(statement).all()


def search_artists(
    *, session: Session, query: str, skip: int = 0, limit: int = 50
) -> list[Artist]:
    """Search artists by name"""
    statement = (
        select(Artist)
        .where(Artist.name.ilike(f"%{query}%"))
        .offset(skip)
        .limit(limit)
        .order_by(Artist.name)
    )
    return session.exec(statement).all()


def update_artist(
    *, session: Session, db_artist: Artist, artist_update: ArtistUpdate
) -> Artist:
    """Update an artist"""
    artist_data = artist_update.model_dump(exclude_unset=True)
    db_artist.sqlmodel_update(artist_data)
    session.add(db_artist)
    session.commit()
    session.refresh(db_artist)
    return db_artist


def delete_artist(*, session: Session, artist_id: UUID) -> bool:
    """Delete an artist"""
    artist = session.get(Artist, artist_id)
    if artist:
        session.delete(artist)
        session.commit()
        return True
    return False


# ===== ALBUM CRUD =====

def create_album(*, session: Session, album_create: AlbumCreate) -> Album:
    """Create a new album"""
    db_obj = Album.model_validate(album_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_album(*, session: Session, album_id: UUID) -> Album | None:
    """Get album by ID"""
    return session.get(Album, album_id)


def get_albums(
    *, session: Session, skip: int = 0, limit: int = 100
) -> list[Album]:
    """Get all albums with pagination"""
    statement = select(Album).offset(skip).limit(limit).order_by(desc(Album.release_date))
    return session.exec(statement).all()


def get_albums_by_artist(
    *, session: Session, artist_id: UUID, skip: int = 0, limit: int = 50
) -> list[Album]:
    """Get albums by artist ID"""
    statement = (
        select(Album)
        .where(Album.artist_id == artist_id)
        .offset(skip)
        .limit(limit)
        .order_by(desc(Album.release_date))
    )
    return session.exec(statement).all()


def search_albums(
    *, session: Session, query: str, skip: int = 0, limit: int = 50
) -> list[Album]:
    """Search albums by title"""
    statement = (
        select(Album)
        .where(Album.title.ilike(f"%{query}%"))
        .offset(skip)
        .limit(limit)
        .order_by(Album.title)
    )
    return session.exec(statement).all()


def update_album(
    *, session: Session, db_album: Album, album_update: AlbumUpdate
) -> Album:
    """Update an album"""
    album_data = album_update.model_dump(exclude_unset=True)
    db_album.sqlmodel_update(album_data)
    session.add(db_album)
    session.commit()
    session.refresh(db_album)
    return db_album


def delete_album(*, session: Session, album_id: UUID) -> bool:
    """Delete an album"""
    album = session.get(Album, album_id)
    if album:
        session.delete(album)
        session.commit()
        return True
    return False


# ===== SONG CRUD =====

def create_song(*, session: Session, song_create: SongCreate) -> Song:
    """Create a new song"""
    db_obj = Song.model_validate(song_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_song(*, session: Session, song_id: UUID) -> Song | None:
    """Get song by ID"""
    return session.get(Song, song_id)


def get_songs(
    *, session: Session, skip: int = 0, limit: int = 100
) -> list[Song]:
    """Get all songs with pagination"""
    statement = select(Song).offset(skip).limit(limit).order_by(Song.title)
    return session.exec(statement).all()


def get_songs_by_album(
    *, session: Session, album_id: UUID, skip: int = 0, limit: int = 100
) -> list[Song]:
    """Get songs by album ID"""
    statement = (
        select(Song)
        .where(Song.album_id == album_id)
        .offset(skip)
        .limit(limit)
        .order_by(Song.track_number)
    )
    return session.exec(statement).all()


def get_songs_by_artist(
    *, session: Session, artist_id: UUID, skip: int = 0, limit: int = 100
) -> list[Song]:
    """Get songs by artist ID"""
    statement = (
        select(Song)
        .where(Song.artist_id == artist_id)
        .offset(skip)
        .limit(limit)
        .order_by(desc(Song.created_at))
    )
    return session.exec(statement).all()


def get_songs_by_genre(
    *, session: Session, genre_id: UUID, skip: int = 0, limit: int = 100
) -> list[Song]:
    """Get songs by genre ID"""
    statement = (
        select(Song)
        .where(Song.genre_id == genre_id)
        .offset(skip)
        .limit(limit)
        .order_by(desc(Song.play_count))
    )
    return session.exec(statement).all()


def search_songs(
    *, session: Session, query: str, skip: int = 0, limit: int = 50
) -> list[Song]:
    """Search songs by title"""
    statement = (
        select(Song)
        .where(Song.title.ilike(f"%{query}%"))
        .offset(skip)
        .limit(limit)
        .order_by(Song.title)
    )
    return session.exec(statement).all()


def get_popular_songs(
    *, session: Session, skip: int = 0, limit: int = 50
) -> list[Song]:
    """Get popular songs ordered by play count"""
    statement = (
        select(Song)
        .offset(skip)
        .limit(limit)
        .order_by(desc(Song.play_count))
    )
    return session.exec(statement).all()


def increment_play_count(*, session: Session, song_id: UUID) -> Song | None:
    """Increment play count for a song"""
    song = session.get(Song, song_id)
    if song:
        song.play_count += 1
        session.add(song)
        session.commit()
        session.refresh(song)
    return song


def update_song(
    *, session: Session, db_song: Song, song_update: SongUpdate
) -> Song:
    """Update a song"""
    song_data = song_update.model_dump(exclude_unset=True)
    db_song.sqlmodel_update(song_data)
    session.add(db_song)
    session.commit()
    session.refresh(db_song)
    return db_song


def delete_song(*, session: Session, song_id: UUID) -> bool:
    """Delete a song"""
    song = session.get(Song, song_id)
    if song:
        session.delete(song)
        session.commit()
        return True
    return False


# ===== PLAYLIST CRUD =====

def create_playlist(*, session: Session, playlist_create: PlaylistCreate, owner_id: UUID) -> Playlist:
    """Create a new playlist"""
    playlist_data = playlist_create.model_dump()
    playlist_data["owner_id"] = owner_id
    db_obj = Playlist.model_validate(playlist_data)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_playlist(*, session: Session, playlist_id: UUID) -> Playlist | None:
    """Get playlist by ID"""
    return session.get(Playlist, playlist_id)


def get_playlists_by_user(
    *, session: Session, user_id: UUID, skip: int = 0, limit: int = 50
) -> list[Playlist]:
    """Get playlists by user ID"""
    statement = (
        select(Playlist)
        .where(Playlist.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(desc(Playlist.updated_at))
    )
    return session.exec(statement).all()


def get_public_playlists(
    *, session: Session, skip: int = 0, limit: int = 50
) -> list[Playlist]:
    """Get public playlists"""
    statement = (
        select(Playlist)
        .where(Playlist.is_public == True)
        .offset(skip)
        .limit(limit)
        .order_by(desc(Playlist.updated_at))
    )
    return session.exec(statement).all()


def search_playlists(
    *, session: Session, query: str, skip: int = 0, limit: int = 50
) -> list[Playlist]:
    """Search public playlists by name"""
    statement = (
        select(Playlist)
        .where(
            and_(
                Playlist.name.ilike(f"%{query}%"),
                Playlist.is_public == True
            )
        )
        .offset(skip)
        .limit(limit)
        .order_by(Playlist.name)
    )
    return session.exec(statement).all()


def add_song_to_playlist(
    *, session: Session, playlist_id: UUID, song_id: UUID, position: int | None = None
) -> PlaylistSong | None:
    """Add a song to playlist"""
    # Get current max position if position not provided
    if position is None:
        max_position_stmt = (
            select(func.max(PlaylistSong.position))
            .where(PlaylistSong.playlist_id == playlist_id)
        )
        max_position = session.exec(max_position_stmt).first()
        position = (max_position or 0) + 1
    
    # Check if song already exists in playlist
    existing_stmt = select(PlaylistSong).where(
        and_(
            PlaylistSong.playlist_id == playlist_id,
            PlaylistSong.song_id == song_id
        )
    )
    existing = session.exec(existing_stmt).first()
    if existing:
        return existing
    
    # Add song to playlist
    playlist_song = PlaylistSong(
        playlist_id=playlist_id,
        song_id=song_id,
        position=position
    )
    session.add(playlist_song)
    session.commit()
    session.refresh(playlist_song)
    return playlist_song


def remove_song_from_playlist(
    *, session: Session, playlist_id: UUID, song_id: UUID
) -> bool:
    """Remove a song from playlist"""
    statement = select(PlaylistSong).where(
        and_(
            PlaylistSong.playlist_id == playlist_id,
            PlaylistSong.song_id == song_id
        )
    )
    playlist_song = session.exec(statement).first()
    if playlist_song:
        session.delete(playlist_song)
        session.commit()
        return True
    return False


def get_playlist_songs(
    *, session: Session, playlist_id: UUID, skip: int = 0, limit: int = 100
) -> list[Song]:
    """Get songs in a playlist"""
    statement = (
        select(Song)
        .join(PlaylistSong)
        .where(PlaylistSong.playlist_id == playlist_id)
        .offset(skip)
        .limit(limit)
        .order_by(PlaylistSong.position)
    )
    return session.exec(statement).all()


def reorder_playlist_songs(
    *, session: Session, playlist_id: UUID, song_positions: list[dict[str, Any]]
) -> bool:
    """Reorder songs in a playlist
    song_positions: [{"song_id": UUID, "position": int}, ...]
    """
    try:
        for item in song_positions:
            song_id = item["song_id"]
            position = item["position"]
            
            statement = select(PlaylistSong).where(
                and_(
                    PlaylistSong.playlist_id == playlist_id,
                    PlaylistSong.song_id == song_id
                )
            )
            playlist_song = session.exec(statement).first()
            if playlist_song:
                playlist_song.position = position
                session.add(playlist_song)
        
        session.commit()
        return True
    except Exception:
        session.rollback()
        return False


def update_playlist(
    *, session: Session, db_playlist: Playlist, playlist_update: PlaylistUpdate
) -> Playlist:
    """Update a playlist"""
    playlist_data = playlist_update.model_dump(exclude_unset=True)
    db_playlist.sqlmodel_update(playlist_data)
    session.add(db_playlist)
    session.commit()
    session.refresh(db_playlist)
    return db_playlist


def delete_playlist(*, session: Session, playlist_id: UUID) -> bool:
    """Delete a playlist"""
    playlist = session.get(Playlist, playlist_id)
    if playlist:
        session.delete(playlist)
        session.commit()
        return True
    return False
