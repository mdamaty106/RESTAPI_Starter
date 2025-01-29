# Flask REST API Template

A robust Flask-based REST API starter template providing foundational infrastructure for building scalable web services.

## Features

- User Authentication with JWT
- Rate Limiting
- PostgreSQL Database Integration
- Redis Cache Support
- CORS Enabled
- Error Handling Middleware
- API Documentation

## Tech Stack

- Flask
- PostgreSQL
- Redis
- JWT Authentication
- SQLAlchemy ORM
- Flask-Marshmallow for serialization

## Getting Started

1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
export FLASK_SECRET_KEY=your_secret_key
export DATABASE_URL=your_database_url
export JWT_SECRET_KEY=your_jwt_secret
export REDIS_URL=your_redis_url  # Optional, defaults to localhost
```

4. Run the application
```bash
python main.py
```

## API Endpoints

### Authentication
- POST `/api/auth/login` - User login
- POST `/api/auth/refresh` - Refresh access token
- POST `/api/auth/logout` - Logout user
- POST `/api/auth/logout-all` - Logout from all devices

### Users
- GET `/api/users/` - Get all users (protected)
- GET `/api/users/<id>` - Get specific user (protected)
- POST `/api/users/register` - Register new user

### Posts
- GET `/api/posts/` - Get all posts
- GET `/api/posts/<id>` - Get specific post
- POST `/api/posts/` - Create new post (protected)
- PUT `/api/posts/<id>` - Update post (protected)
- DELETE `/api/posts/<id>` - Delete post (protected)

## Security Features

- Password Hashing
- JWT Token Authentication
- Rate Limiting
- Input Validation
- CORS Protection
- SQL Injection Prevention through SQLAlchemy

## License

MIT License
