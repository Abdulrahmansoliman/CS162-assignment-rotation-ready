# Minerva Rotation Cities Helper

A full-stack web application helping Minerva University students manage and share rotation city items.

## Architecture

- **Backend**: Flask REST API with SQLAlchemy ORM, JWT authentication
- **Frontend**: React + Vite
- **Database**: SQLite (development), PostgreSQL-ready
- **Testing**: Pytest with 230+ tests

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Backend runs at `http://localhost:5000`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

## 📚 API Documentation

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/verify` - Email verification

### Resources
- `GET /api/v1/category/` - List all categories
- `GET /api/v1/item/` - List all items
- `GET /api/v1/tag/` - List all tags
- `GET /api/v1/value/tag/<tag_id>` - Get text values for tag
- `GET /api/v1/rotation-city/` - List rotation cities

All resource endpoints require JWT authentication via `Authorization: Bearer <token>` header.

## 🧪 Testing

```bash
cd backend
pytest                    # Run all tests
pytest tests/unit/        # Unit tests only
pytest tests/integration/ # Integration tests only
```

## 📁 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/v1/          # REST endpoints
│   │   ├── models/          # SQLAlchemy models
│   │   ├── services/        # Business logic
│   │   ├── repositories/    # Data access layer
│   │   └── config/          # Environment configs
│   ├── tests/
│   └── run.py
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   └── services/
    └── package.json
```

## � Documentation

For comprehensive documentation, visit the **[Project Wiki](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki)**:

- **[Quick Start Guide](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki/Quick-Start-Guide)** - Get up and running in 10 minutes
- **[API Documentation](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki/API-Documentation)** - Complete REST API reference
- **[Database Schema](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki/Database-Schema)** - Database design and relationships
- **[Backend Development](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki/Backend-Development)** - Backend architecture guide
- **[Frontend Development](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki/Frontend-Development)** - Frontend development guide
- **[Testing Guide](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki/Testing-Guide)** - How to write and run tests
- **[Deployment Guide](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki/Deployment-Guide)** - Production deployment instructions
- **[Project Structure](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki/Project-Structure)** - Codebase organization

Also see:
- [backend/README.md](backend/README.md) - Backend setup and development
- [backend/TESTING.md](backend/TESTING.md) - Testing guidelines
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment configuration
