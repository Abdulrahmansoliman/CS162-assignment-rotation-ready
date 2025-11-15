# Backend Setup Instructions

## Prerequisites
- Python 3.11+ installed

## Setup Steps

### 1. Create Virtual Environment
```powershell
cd backend
python -m venv venv
```

### 2. Install Dependencies
```powershell
.\venv\bin\pip install -r requirements.txt
```

### 3. Initialize Database
```powershell
.\venv\bin\python -c "from app.models import create_all_tables; create_all_tables()"
```

## Usage

### Import Models
```python
from app.models import (
    User, RotationCity, Item, Category,
    CategoryItem, Verification, Tag, Value, ItemTagValue
)
```

### Create Database Session
```python
from app.db import SessionLocal

db = SessionLocal()
# ... your database operations
db.close()
```

### Create Tables
```python
from app.models import create_all_tables
create_all_tables()
```

### Drop Tables (WARNING: Deletes all data!)
```python
from app.models import drop_all_tables
drop_all_tables()
```

## Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── db.py              # Database configuration
│   └── models/
│       ├── __init__.py    # Model exports & DB functions
│       ├── user.py
│       ├── rotation_city.py
│       ├── category.py
│       ├── item.py
│       ├── category_item.py
│       ├── verification.py
│       ├── tag.py
│       ├── value.py
│       └── item_tag_value.py
├── requirements.txt
└── app.db                 # SQLite database (created after setup)
```
