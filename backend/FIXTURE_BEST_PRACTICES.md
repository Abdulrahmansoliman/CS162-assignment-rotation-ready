# Fixture Best Practices Guide

## Core Principles

### **1. Organize by Domain**
```
tests/fixtures/
├── user_fixtures.py          # User, RotationCity
├── item_fixtures.py          # Item, Category
├── verification_fixtures.py  # VerificationCode
└── auth_fixtures.py          # Auth-related (future)
```

### **2. Fixture Scope Hierarchy**
```
Session Scope (app)
    ↓
Function Scope (db_session, user, item, etc.)
    ↓
Each Test Gets Fresh Data
```

### **3. Dependency Chain**
```
app (session scope)
  └── db_session (function scope)
      ├── rotation_city (uses db_session)
      ├── user (uses db_session, rotation_city)
      └── verification_code (uses db_session, user)
```

---

## Best Practices

### ✅ **DO: Refresh Objects After Commit**
```python
@pytest.fixture
def user(db_session, rotation_city):
    user = User(...)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)  # ← Refresh to get fresh instance
    return user
```

**Why**: After `commit()`, SQLAlchemy might have modified the object. Refresh ensures you get the actual database state.

### ✅ **DO: Include All Required Fields**
```python
# ✅ Complete fixture with all fields
code = VerificationCode(
    user_id=user.user_id,
    code_hash='abc123hash',
    hash_salt='abc123salt',        # ← Required field
    code_type=VerificationCodeType.REGISTRATION.code,  # ← Use .code property
    created_at=now,                # ← Include timestamps
    expires_at=now + timedelta(minutes=15),
    attempts=0,
    is_used=False
)
```

### ✅ **DO: Use Enum Properties Correctly**
```python
# ✅ Correct - Use enum's .code property
code_type=VerificationCodeType.REGISTRATION.code

# ❌ Wrong - Using enum directly
code_type=VerificationCodeType.REGISTRATION
```

### ✅ **DO: Create Variations for Different Scenarios**
```python
@pytest.fixture
def verification_code(db_session, user):
    """Default: unused, no attempts"""
    ...

@pytest.fixture
def used_verification_code(db_session, user):
    """Already verified"""
    ...

@pytest.fixture
def expired_code(db_session, user):
    """Past expiration time"""
    ...

@pytest.fixture
def max_attempts_code(db_session, user):
    """Maximum attempts reached"""
    ...
```

### ✅ **DO: Document Fixture Purpose**
```python
@pytest.fixture
def verified_user(db_session, rotation_city):
    """Create a verified test user.
    
    This fixture represents a user who has completed
    the registration verification process.
    
    Use for:
    - Testing login flows
    - Testing authenticated endpoints
    - Testing verification updates
    """
    ...
```

### ❌ **DON'T: Skip Timestamps**
```python
# ❌ Bad - Missing timestamps
code = VerificationCode(
    user_id=user.user_id,
    code_hash='hash',
    # No created_at or expires_at!
)

# ✅ Good - Include timestamps
now = datetime.utcnow()
code = VerificationCode(
    user_id=user.user_id,
    code_hash='hash',
    created_at=now,
    expires_at=now + timedelta(minutes=15)
)
```

### ❌ **DON'T: Use Raw Enum Values**
```python
# ❌ Wrong - Assigns enum object instead of code
code_type=VerificationCodeType.REGISTRATION

# ✅ Correct - Use .code property
code_type=VerificationCodeType.REGISTRATION.code
```

### ❌ **DON'T: Forget to Commit and Refresh**
```python
# ❌ Bad - Object not in database
user = User(...)
db_session.add(user)
return user  # ← Not committed!

# ✅ Good - Committed and refreshed
user = User(...)
db_session.add(user)
db_session.commit()
db_session.refresh(user)
return user
```

---

## Fixture Patterns

### **Pattern 1: Basic Entity**
```python
@pytest.fixture
def rotation_city(db_session):
    """Create a test rotation city."""
    city = RotationCity(
        name='San Francisco',
        time_zone='America/Los_Angeles',
        res_hall_location='Downtown Dorm'
    )
    db_session.add(city)
    db_session.commit()
    db_session.refresh(city)
    return city
```

### **Pattern 2: Dependent Entity**
```python
@pytest.fixture
def user(db_session, rotation_city):
    """Create a test user (depends on rotation_city)."""
    user = User(
        first_name='John',
        last_name='Doe',
        email='john@example.com',
        rotation_city_id=rotation_city.city_id,
        # ... other fields
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
```

### **Pattern 3: Variations**
```python
@pytest.fixture
def user(db_session, rotation_city):
    """Default user - unverified"""
    return _create_user(db_session, rotation_city, 
                       is_verified=False, 
                       status=VerificationStatusEnum.PENDING.code)

@pytest.fixture
def verified_user(db_session, rotation_city):
    """Verified user"""
    return _create_user(db_session, rotation_city,
                       is_verified=True,
                       status=VerificationStatusEnum.VERIFIED.code)

def _create_user(db_session, rotation_city, **kwargs):
    """Helper to create users with custom attributes."""
    user = User(
        rotation_city_id=rotation_city.city_id,
        first_name='Test',
        last_name='User',
        email=kwargs.get('email', f'test{id(user)}@example.com'),
        **kwargs
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
```

### **Pattern 4: Using App Context**
```python
@pytest.fixture
def max_attempts_code(db_session, user, app_context):
    """Code with max attempts (needs app_context for config)."""
    from flask import current_app
    max_attempts = current_app.config.get('MAX_VERIFICATION_ATTEMPTS', 5)
    
    code = VerificationCode(
        user_id=user.user_id,
        code_hash='maxattempts123hash',
        hash_salt='maxattempts123salt',
        attempts=max_attempts,
        # ... other fields
    )
    db_session.add(code)
    db_session.commit()
    db_session.refresh(code)
    return code
```

---

## Testing Your Fixtures

### **Test that fixture works**
```python
@pytest.mark.unit
class TestVerificationCodeFixture:
    def test_verification_code_fixture(self, verification_code):
        """Verify the fixture creates a valid code."""
        assert verification_code.id is not None
        assert verification_code.is_used is False
        assert verification_code.code_hash == 'abc123hash'
```

---

## Summary Checklist

✅ Organize fixtures by domain  
✅ Refresh objects after commit  
✅ Include all required fields  
✅ Use enum properties correctly (.code)  
✅ Add timestamps (created_at, expires_at)  
✅ Create variations for different scenarios  
✅ Document fixture purpose  
✅ Import in conftest.py  
✅ Use db_session for test isolation  
✅ Commit before returning  

Your fixtures are now **production-ready** and follow best practices! 🚀
