# Music App - Full Stack Platform

🎵 **A modern music streaming platform built with FastAPI and React**

## ✨ Features

### 🎧 **Music Streaming**
- Browse artists, albums, and songs
- Create and manage playlists
- High-quality audio streaming
- Search across all music content

### 👥 **Social Features**
- Follow your favorite artists
- Like songs, albums, and playlists
- Build your personal music library
- User listening statistics

### 🎤 **Artist Platform**
- Artist profiles and verification
- Upload and manage music content
- Track play counts and analytics
- Album and song management

### 🔐 **Security & Auth**
- JWT authentication
- Role-based permissions (User/Artist/Admin)
- Secure file uploads
- Password recovery via email

## 🛠️ Technology Stack

### **Backend**
- ⚡ **FastAPI** - Modern Python web framework
- 🧰 **SQLModel** - Database ORM with type safety
- 💾 **PostgreSQL** - Reliable SQL database
- 🔑 **JWT** - Secure authentication
- 🐋 **Docker** - Containerized deployment

### **Frontend**
- 🚀 **React** - Modern UI framework
- 💃 **TypeScript** - Type-safe development
- 🎨 **Chakra UI** - Beautiful components
- ⚡ **Vite** - Fast development server

### **Infrastructure**
- 🐋 **Docker Compose** - Multi-service orchestration
- 📞 **Traefik** - Reverse proxy & load balancer
- 📧 **Email** - Password recovery system
- ✅ **Testing** - Comprehensive test suite

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Setup
```bash
# Clone repository
git clone <repository-url> music-app
cd music-app

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start services
docker-compose up -d
```

### Access
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database Admin**: http://localhost:8080

### Default Admin Account
- **Email**: admin@musicapp.com
- **Password**: Admin123!

## 📱 API Endpoints

### **Public APIs**
```
GET  /api/v1/songs           # Browse songs
GET  /api/v1/artists         # Browse artists  
GET  /api/v1/search/all      # Search content
GET  /api/v1/discover/       # Discover new music
```

### **User APIs** (Authentication Required)
```
POST /api/v1/social/like     # Like content
POST /api/v1/playlists       # Create playlists
POST /api/v1/files/upload    # Upload files
GET  /api/v1/play/stats      # User statistics
```

### **Artist APIs** (Artist/Admin Only)
```
POST /api/v1/songs           # Upload songs
POST /api/v1/albums          # Create albums
PATCH /api/v1/artists/{id}   # Update artist profile
```

### **Admin APIs** (Admin Only)
```
POST /api/v1/users           # User management
POST /api/v1/genres          # Manage genres
DELETE /api/v1/files/{id}    # Content moderation
```

## 🎯 Core Features

### **Music Management**
- Upload MP3, WAV, FLAC files
- Automatic metadata extraction
- Cover art management
- Genre categorization

### **User Experience**
- Responsive web player
- Playlist management
- Music discovery algorithms
- Social interactions

### **Analytics**
- Play count tracking
- User listening history
- Artist performance metrics
- Popular content insights

## 🔧 Development

### **Backend Development**
```bash
cd backend
# See backend/README.md for details
```

### **Frontend Development**
```bash
cd frontend  
# See frontend/README.md for details
```

### **Database Management**
```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"
```

## 🚀 Deployment

### **Production Setup**
```bash
# Configure production environment
cp .env.example .env.production

# Deploy with Docker Compose
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### **Environment Variables**
```env
# Security
SECRET_KEY=your-secret-key
POSTGRES_PASSWORD=secure-db-password

# Admin Account  
FIRST_SUPERUSER=admin@yourdomain.com
FIRST_SUPERUSER_PASSWORD=secure-admin-password

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

🎵 **Built for music lovers, by music lovers** 🎵
