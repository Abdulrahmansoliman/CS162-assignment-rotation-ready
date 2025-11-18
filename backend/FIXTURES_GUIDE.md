# conftest.py vs fixtures/ Organization Guide

## Overview

### conftest.py
**Location**: `tests/conftest.py`

**Purpose**: 
- Pytest automatically discovers and loads this file
- Entry point for all test configurations and infrastructure

**What goes here**:
- ✅ Core infrastructure (app, db, client, app_context)
- ✅ Pytest hooks and plugins
- ✅ Global configuration
- ✅ Import statements for fixture packages

**Scope**: Available to ALL tests in this directory and subdirectories

```python
# conftest.py - Keep it clean and focused
import pytest
from app import create_app, db
from tests.fixtures.user_fixtures import *

@pytest.fixture(scope='session')
def app():
    """Infrastructure fixture"""
    ...
```

---

### fixtures/ Directory
**Location**: `tests/fixtures/`

**Purpose**: 
- Organize domain-specific fixtures by feature/component
- Keep conftest.py clean and readable
- Easier to find fixture definitions

**What goes here**:
- ✅ Model fixtures (user, item, category, etc.)
- ✅ Domain-specific fixtures (auth, verification, etc.)
- ✅ Multiple variations of entities (verified_user, unverified_user, etc.)

**Structure**:
```
tests/fixtures/
├── __init__.py
├── user_fixtures.py          # User, RotationCity, variations
├── item_fixtures.py          # Item, Category, CategoryItem
└── verification_fixtures.py  # VerificationCode, variations
```

---

## Benefits of This Approach

| Aspect | conftest.py | fixtures/ |
|--------|-------------|-----------|
| **Size** | Small, focused | Organized by domain |
| **Discoverability** | Auto-loaded | Import needed |
| **Scope** | Everything | Specific features |
| **Readability** | Quick overview | Detailed, searchable |
| **Maintenance** | Less cluttered | Domain-organized |

---

## Example Usage

### In conftest.py
```python
from tests.fixtures.user_fixtures import *
from tests.fixtures.item_fixtures import *
from tests.fixtures.verification_fixtures import *

@pytest.fixture(scope='session')
def app():
    # Infrastructure only
    pass

@pytest.fixture
def db_session(app):
    # Infrastructure only
    pass
```

### In test files
```python
def test_user_creation(user):
    # Automatically gets user fixture from user_fixtures.py
    assert user.email == 'john@example.com'

def test_item_with_category(item, category):
    # Gets fixtures from item_fixtures.py
    assert item.category_items
```

---

## Available Fixtures

### User Fixtures (`user_fixtures.py`)
- `rotation_city` - Test rotation city
- `user` - Default test user
- `unverified_user` - Unverified user variant
- `verified_user` - Verified user variant

### Item Fixtures (`item_fixtures.py`)
- `category` - Electronics category
- `furniture_category` - Furniture category variant
- `item` - Test item with category
- `book` - Book item variant

### Verification Fixtures (`verification_fixtures.py`)
- `verification_code` - Unused code
- `used_verification_code` - Already used variant
- `max_attempts_code` - Maxed out attempts variant
- `login_code` - Login type code

---

## Adding New Fixtures

1. **Identify the domain** (user, item, auth, etc.)
2. **Create or update the fixture file**:
   ```python
   # tests/fixtures/auth_fixtures.py
   @pytest.fixture
   def user_with_token(user):
       token = generate_token(user)
       return user, token
   ```

3. **Import in conftest.py**:
   ```python
   from tests.fixtures.auth_fixtures import *
   ```

4. **Use in tests**:
   ```python
   def test_auth(user_with_token):
       user, token = user_with_token
   ```

---

## Best Practices

✅ **Do**:
- Keep conftest.py focused on infrastructure
- Organize fixtures by domain/feature
- Use descriptive names (verified_user, unverified_user)
- Create fixture variations for different scenarios
- Document fixture purpose in docstrings

❌ **Don't**:
- Overload conftest.py with fixtures
- Mix infrastructure and model fixtures
- Create vague fixture names
- Duplicate fixture logic across files

---

## File Organization Summary

```
tests/
├── conftest.py                    # Infrastructure & imports
├── fixtures/
│   ├── __init__.py
│   ├── user_fixtures.py          # User domain
│   ├── item_fixtures.py          # Item domain
│   └── verification_fixtures.py  # Verification domain
├── unit/
│   ├── api/
│   ├── services/
│   ├── repositories/
│   └── models/
└── integration/
```

This keeps your test infrastructure organized, maintainable, and easy to navigate! 🎯
