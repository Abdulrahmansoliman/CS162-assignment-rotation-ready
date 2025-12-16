# Backend - Rotation Ready API

Flask REST API for the Rotation Ready application, providing endpoints for user authentication, item management, and city-specific listings for Minerva University students.

## Quick Start

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Server runs at `http://localhost:5000`

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Database Setup](#database-setup)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development Guide](#development-guide)

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment tool (venv)
- SQLite (development) or PostgreSQL (production)

## Installation

### 1. Create Virtual Environment

**macOS/Linux:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
```

**Windows (Command Prompt):**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate.bat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required variables:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///instance/app.db
CORS_ORIGINS=http://localhost:5173
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
FRONTEND_URL=http://localhost:5173
```

Generate secure keys:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Initialize Database

```bash
python -c "from app.models import create_all_tables; create_all_tables()"
```

### 5. (Optional) Seed Sample Data

```bash
python seed/seed.py
```

## Configuration

Configuration is managed through environment-specific config files in `app/config/`:

- `base.py` - Base configuration
- `development.py` - Development settings (SQLite, debug mode)
- `production.py` - Production settings (PostgreSQL, no debug)
- `testing.py` - Test settings (in-memory SQLite)

## Running the Application

### Development Server

```bash
python run.py
```

The API will be available at `http://localhost:5000`

### Production Server

```bash
gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 "app:create_app('production')"
```

## Database Setup

### Create All Tables

```python
from app.models import create_all_tables
create_all_tables()
```

### Drop All Tables (WARNING: Deletes all data!)

```python
from app.models import drop_all_tables
drop_all_tables()
```

### Working with the Database

```python
from app.db import SessionLocal
from app.models import User, Item, Category

# Create session
db = SessionLocal()

# Query examples
users = db.query(User).all()
user = db.query(User).filter_by(email="test@example.com").first()

# Create new record
new_user = User(email="new@example.com", password_hash="...")
db.add(new_user)
db.commit()

# Always close session
db.close()
```

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# API tests
pytest -m api

# With coverage report
pytest --cov=app --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/integration/test_auth_routes.py
```

See [TESTING.md](TESTING.md) for comprehensive testing documentation.

## API Documentation

### Base URL

Development: `http://localhost:5000/api/v1`

### Authentication

Most endpoints require JWT authentication. Include token in header:
```
Authorization: Bearer <your_token>
```

### Key Endpoints

**Authentication:**
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/verify` - Verify email with code

**Items:**
- `GET /api/v1/item/` - List all items
- `POST /api/v1/item/` - Create new item
- `GET /api/v1/item/<id>` - Get item details
- `PUT /api/v1/item/<id>` - Update item
- `DELETE /api/v1/item/<id>` - Delete item

**Categories:**
- `GET /api/v1/category/` - List all categories
- `GET /api/v1/category/<id>` - Get category details

**Cities:**
- `GET /api/v1/rotation-city/` - List all rotation cities

**Tags & Values:**
- `GET /api/v1/tag/` - List all tags
- `GET /api/v1/value/tag/<tag_id>` - Get values for a tag

For complete API documentation, see the [GitHub Wiki](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki/API-Documentation).

## Project Structure

```
backend/
├── app/
│   ├── __init__.py              # Application factory
│   ├── api/                      # API routes
│   │   └── v1/                   # API version 1
│   │       ├── __init__.py       # Blueprint registration
│   │       ├── auth/             # Authentication routes
│   │       ├── schemas/          # Pydantic validation schemas
│   │       ├── category.py       # Category endpoints
│   │       ├── item.py           # Item endpoints
│   │       ├── rotation_city.py  # City endpoints
│   │       ├── tag.py            # Tag endpoints
│   │       ├── user.py           # User endpoints
│   │       ├── value.py          # Value endpoints
│   │       └── verification.py   # Verification endpoints
│   │
│   ├── config/                   # Configuration files
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   │
│   ├── models/                   # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── item.py
│   │   ├── category.py
│   │   ├── rotation_city.py
│   │   ├── tag.py
│   │   └── value.py
│   │
│   ├── repositories/             # Data access layer
│   │   ├── base/
│   │   │   └── base_repository.py
│   │   └── implementations/
│   │       ├── user_repository.py
│   │       ├── item_repository.py
│   │       └── ...
│   │
│   ├── services/                 # Business logic layer
│   │   ├── auth/
│   │   │   ├── login_service.py
│   │   │   ├── registration_service.py
│   │   │   └── token_service.py
│   │   ├── email/
│   │   │   └── email_service.py
│   │   ├── category_service.py
│   │   ├── item_service.py
│   │   └── ...
│   │
│   └── utils/                    # Utility functions
│       └── decorators.py
│
├── tests/                        # Test suite
│   ├── conftest.py              # Pytest fixtures
│   ├── fixtures/                # Test data fixtures
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
│
├── seed/                        # Database seeding
│   └── seed.py
│
├── instance/                    # Instance-specific files
│   └── app.db                   # SQLite database (gitignored)
│
├── requirements.txt             # Python dependencies
├── run.py                      # Application entry point
├── pytest.ini                  # Pytest configuration
├── Procfile                    # Deployment process file
├── runtime.txt                 # Python version
├── TESTING.md                  # Testing guide
└── README.md                   # This file
```

## Development Guide

### Architecture

The backend follows a layered architecture:

1. **API Layer** (`app/api/v1/`) - HTTP request/response handling
2. **Service Layer** (`app/services/`) - Business logic
3. **Repository Layer** (`app/repositories/`) - Data access
4. **Model Layer** (`app/models/`) - Database schema

### Adding a New Endpoint

1. **Create route** in `app/api/v1/your_resource.py`
2. **Add schema** in `app/api/v1/schemas/your_schemas.py`
3. **Implement service** in `app/services/your_service.py`
4. **Create repository** if needed in `app/repositories/implementations/`
5. **Write tests** in `tests/integration/test_your_routes.py`

### Code Style

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Example: Creating a New Endpoint

```python
# app/api/v1/example.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.example_service import ExampleService
from app.db import SessionLocal

example_bp = Blueprint('example', __name__, url_prefix='/example')

@example_bp.route('/', methods=['GET'])
@jwt_required()
def get_examples():
    """Get all examples."""
    db = SessionLocal()
    try:
        service = ExampleService(db)
        examples = service.get_all()
        return jsonify({'examples': [e.to_dict() for e in examples]}), 200
    finally:
        db.close()
```

## Dependencies

Key dependencies:

- **Flask 3.0.0** - Web framework
- **SQLAlchemy 2.0.23** - ORM
- **Flask-JWT-Extended 4.6.0** - JWT authentication
- **Flask-CORS 4.0.0** - CORS support
- **Flask-Mail 0.10.0** - Email sending
- **Pydantic 2.5.0** - Data validation
- **Gunicorn 21.2.0** - Production WSGI server
- **Pytest 7.4.3** - Testing framework

See `requirements.txt` for complete list.

## Common Issues

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

### Database Migration Errors

```bash
# Reset database (WARNING: Deletes all data)
rm instance/app.db
python -c "from app.models import create_all_tables; create_all_tables()"
```

### Import Errors

Ensure virtual environment is activated:
```bash
which python  # Should point to venv/bin/python
```

## Contributing

1. Follow the existing code structure
2. Write tests for new features
3. Update documentation
4. Follow PEP 8 style guide
5. Add type hints

## License

This project is part of CS162 at Minerva University.

## Additional Resources

- [GitHub Wiki](https://github.com/Abdulrahmansoliman/CS162-assignment-rotation-ready/wiki) - Comprehensive documentation
- [TESTING.md](TESTING.md) - Testing guide
- [DEPLOYMENT.md](../DEPLOYMENT.md) - Deployment instructions
