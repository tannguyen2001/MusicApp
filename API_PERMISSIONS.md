# Music App API

## Giới thiệu
Music App là ứng dụng streaming nhạc được xây dựng với FastAPI và React.

## Tính năng chính
- Upload và streaming nhạc
- Quản lý playlist cá nhân
- Tìm kiếm nghệ sĩ, album, bài hát
- Hệ thống follow/like/library
- Thống kê nghe nhạc

## Công nghệ
- **Backend**: FastAPI, SQLModel, PostgreSQL, Alembic
- **Frontend**: React, TypeScript, Vite
- **Infrastructure**: Docker, Docker Compose

## API Endpoints

### Công khai
- `GET /songs` - Danh sách bài hát
- `GET /artists` - Danh sách nghệ sĩ  
- `GET /search/*` - Tìm kiếm
- `GET /files/songs/{id}` - Stream nhạc

### Cần đăng nhập
- `POST /social/like` - Like bài hát
- `POST /playlists` - Tạo playlist
- `POST /files/upload/song` - Upload nhạc

### Chỉ Admin
- `POST /genres` - Tạo thể loại
- `DELETE /users/{id}` - Xóa user

## Chạy dự án
```bash
docker-compose up
```

Truy cập: http://localhost:8000/docs
