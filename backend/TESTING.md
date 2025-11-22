# Testing Guide

## Setup

### Install Testing Dependencies
```bash
pip install -r requirements.txt
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/unit/test_user.py
```

### Run Specific Test Class
```bash
pytest tests/unit/test_user.py::TestUserRepository
```

### Run Specific Test
```bash
pytest tests/unit/test_user.py::TestUserRepository::test_create_user
```

### Run Tests by Component
```bash
# Run only API tests
pytest -m api

# Run only service tests
pytest -m service

# Run only repository tests
pytest -m repository

# Run only model tests
pytest -m model

# Run all unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only auth tests
pytest -m auth
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage Report
```bash
pytest --cov=app --cov-report=html
# Reports generate in htmlcov/index.html
```

## Test Organization

```
tests/
├── conftest.py                     # Shared fixtures and configuration
├── __init__.py
├── unit/                           # Unit tests (organized by component)
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── test_endpoints.py       # API endpoint tests
│   ├── services/
│   │   ├── __init__.py
│   │   └── test_verification_code_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── test_user_repository.py
│   └── models/
│       ├── __init__.py
│       └── test_models.py
├── integration/                    # Integration tests
│   ├── __init__.py
│   └── test_auth.py
└── fixtures/                       # Reusable test data
    └── __init__.py
```

## Available Fixtures

All fixtures are defined in `conftest.py`:

### Core Fixtures
- `app` - Flask application instance (session scope)
- `client` - Test client for making requests
- `app_context` - Application context
- `db_session` - Database session (isolated per test)

### Model Fixtures
- `rotation_city` - Test RotationCity instance
- `user` - Test User instance
- `category` - Test Category instance
- `item` - Test Item instance with category
- `tag` - Test Tag instance
- `verification_code` - Test VerificationCode instance

## Using Fixtures in Tests

```python
@pytest.mark.unit
class TestUser:
    def test_something(self, user, db_session):
        # user fixture is automatically injected
        assert user.email == 'john@example.com'
```

## Test Markers

Available markers defined in `pytest.ini`:
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.api` - API endpoint tests
- `@pytest.mark.service` - Service layer tests
- `@pytest.mark.repository` - Repository layer tests
- `@pytest.mark.model` - Model/Database tests
- `@pytest.mark.auth` - Authentication tests
- `@pytest.mark.db` - Database tests
- `@pytest.mark.slow` - Long-running tests
- `@pytest.mark.skip_ci` - Skip in CI environment

## Best Practices

1. **Test Naming**: Use descriptive names like `test_user_creation`
2. **Assertions**: Use clear, specific assertions
3. **Isolation**: Each test should be independent
4. **Fixtures**: Use fixtures instead of setup/teardown
5. **Markers**: Mark tests appropriately for organization
6. **Coverage**: Aim for >80% code coverage

## Example Test

```python
@pytest.mark.unit
@pytest.mark.db
class TestUserCreation:
    def test_create_user_with_valid_data(self, db_session, rotation_city):
        """Test creating a user with valid data."""
        user = User(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.user_id is not None
        assert user.email == 'john@example.com'
```

## Continuous Integration

To run tests in CI (GitHub Actions, etc.):
```bash
pytest -m "not skip_ci" --cov=app
```
