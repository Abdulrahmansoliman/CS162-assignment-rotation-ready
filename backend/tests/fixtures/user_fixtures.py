"""
User and Rotation City Fixtures
"""
import pytest
from app.models import User, RotationCity, VerificationStatusEnum


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


@pytest.fixture
def user(db_session, rotation_city):
    """Create a test user."""
    user = User(
        first_name='John',
        last_name='Doe',
        email='john@example.com',
        rotation_city_id=rotation_city.city_id,
        is_verified=False,
        status=VerificationStatusEnum.PENDING.code
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def unverified_user(db_session, rotation_city):
    """Create an unverified test user."""
    user = User(
        first_name='Jane',
        last_name='Smith',
        email='jane@example.com',
        rotation_city_id=rotation_city.city_id,
        is_verified=False,
        status=VerificationStatusEnum.PENDING.code
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def verified_user(db_session, rotation_city):
    """Create a verified test user."""
    user = User(
        first_name='Bob',
        last_name='Johnson',
        email='bob@example.com',
        rotation_city_id=rotation_city.city_id,
        is_verified=True,
        status=VerificationStatusEnum.VERIFIED.code
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def second_user(db_session, rotation_city):
    """Create a second verified test user."""
    user = User(
        first_name='Alice',
        last_name='Williams',
        email='alice@example.com',
        rotation_city_id=rotation_city.city_id,
        is_verified=True,
        status=VerificationStatusEnum.VERIFIED.code
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
