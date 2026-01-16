# 🎬 Movie Watchlist API

A complete FastAPI application for managing movie watchlists with user and admin roles, featuring authentication, movie management, and genre-based search.

## ✨ Features

### 👥 User Features

- ✅ User registration and JWT authentication
- ✅ View personal watchlist
- ✅ Add/remove movies from watchlist
- ✅ Browse all available movies
- ✅ Search movies by genre (case-insensitive)

### 🎬 Admin Features

- ✅ Admin registration (requires manual setup)
- ✅ Add new movies to the database
- ✅ Manage movie catalog
- ✅ View all movies with admin privileges

### 🔒 Security

- ✅ Password hashing with bcrypt
- ✅ JWT token-based authentication
- ✅ Role-based access control (User/Admin)
- ✅ Protected endpoints with proper authorization

## 🏗️ Technology Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database (can be changed to PostgreSQL/MySQL)
- **JWT** - JSON Web Tokens for authentication
- **Pydantic** - Data validation and settings management
- **Python-dotenv** - Environment configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**

2. **Create a virtual environment**

```bash
python -m venv venv
```

1. **Activate the virtual environment**
   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

1. **Set up environment variables**
   - Update the SECRET_KEY in `.env`:

     ```env
     DATABASE_URL=sqlite:///./movies.db
     SECRET_KEY=your-secret-key
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```

4. **Run the application**

```bash
# Option 1: Using uvicorn directly
uvicorn app.main:app --reload
```

The API will be available at: <http://localhost:8000>

## 📚 API Documentation

Once the server is running, you can access:

- **Doc:** <http://localhost:8000/docs>

## 🔐 Authentication

### Register a User

```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
          "username": "john_doe",
          "email": "john@example.com",
          "password": "securepassword123"
        }'
```

### Login

```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=securepassword123"
```

Response includes an access token:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

## 📋 API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| POST   | /register | Register a new user |
| POST   | /login | Login and get access token |
| GET    | /movies/ | Get all available movies |
| GET    | /movies/search | Search movies by genre (use query params, e.g., `?genre=Animation`) |
| GET    | /movies/{movie_id} | Get specific movie details by ID |

---

### User Endpoints (Authentication Required)

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET    | /users/me | Get current user info |
| GET    | /users/watchlist | Get the current user's watchlist |
| POST   | /users/watchlist/{movie_id} | Add a movie to the user's watchlist |
| DELETE | /users/watchlist/{movie_id} | Remove a movie from the user's watchlist |

---

### Admin Endpoints (Admin Role Required)

| Method | Endpoint | Description |
|--------|---------|-------------|
| POST   | /admin/movies/ | Add a new movie to the database |
| GET    | /admin/movies/ | Get all movies (admin view, may include who added each movie) |

---

### Notes

- **Authentication:** User and Admin endpoints require a JWT access token in the `Authorization` header:  

## 🎯 Usage Examples

### 1. Search Movies by Genre

```bash
curl "http://localhost:8000/movies/search?genre=action"
```

### 2. Add Movie to Watchlist (Authenticated)

```bash
curl -X POST "http://localhost:8000/users/watchlist/1" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Admin - Add New Movie

```bash
curl -X POST "http://localhost:8000/admin/movies/" \
     -H "Authorization: Bearer ADMIN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
          "title": "Inception",
          "genre": "Sci-Fi Thriller",
          "description": "A thief who steals corporate secrets...",
          "year": 2010,
          "director": "Christopher Nolan",
          "duration_minutes": 148
        }'
```

## 👨‍💼 Admin Setup

### Method 1: Database Update (Recommended)

1. Register a regular user
2. Update the user's `is_admin` field to `True` in the database:

```sql
UPDATE users SET is_admin = 1 WHERE username = 'admin_username';
```

## 🔧 Configuration

### Database

The application uses SQLite by default. To use PostgreSQL or MySQL:

1. Update `DATABASE_URL` in `.env`:

```env
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/moviedb

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost/moviedb
```

1. Install the appropriate database driver:

```bash
# For PostgreSQL
pip install psycopg2-binary

# For MySQL
pip install pymysql
```

### Security

- Always change the `SECRET_KEY` in production
- Adjust `ACCESS_TOKEN_EXPIRE_MINUTES` as needed
- Use HTTPS in production environments

## 🌟 Features to Add

Potential future enhancements:

- [ ] Movie ratings and reviews
- [ ] Movie recommendations
- [ ] User profiles
- [ ] Social features (friends, sharing watchlists)
- [ ] Advanced search filters

---
