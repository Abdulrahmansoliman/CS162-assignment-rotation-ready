"""
Unit tests for Item model
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import db
from app.models.item import Item
from app.models.user import User
from app.models.rotation_city import RotationCity


@pytest.fixture(scope='module')
def engine():
    """Create test database engine"""
    engine = create_engine('sqlite:///:memory:')
    db.Model.metadata.create_all(engine)
    yield engine
    db.Model.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope='function')
def session(engine):
    """Create a new database session for a test"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Clear all tables before each test
    for table in reversed(db.Model.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def user(session):
    """Create a test user with rotation city"""
    city = RotationCity(
        name="Test City",
        time_zone="UTC"
    )
    session.add(city)
    session.commit()
    
    user = User(
        rotation_city_id=city.city_id,
        first_name="Test",
        last_name="User",
        username="testuser",
        email="test@example.com"
    )
    session.add(user)
    session.commit()
    return user


class TestItem:
    """Test cases for Item model"""

    def test_create_item(self, session, user):
        """Test creating an item"""
        item = Item(
            added_by_user_id=user.user_id,
            name="Grocery Store",
            location="123 Main St",
            walking_distance=5.5
        )
        session.add(item)
        session.commit()

        assert item.item_id is not None
        assert item.name == "Grocery Store"
        assert item.location == "123 Main St"
        assert item.walking_distance == 5.5

    def test_item_defaults(self, session, user):
        """Test default values for item"""
        item = Item(
            added_by_user_id=user.user_id,
            name="Library",
            location="456 Oak Ave"
        )
        session.add(item)
        session.commit()

        assert item.number_of_verifications == 0
        assert item.last_verified_date is None
        assert isinstance(item.created_at, datetime)

    def test_relationship_to_user(self, session, user):
        """Test relationship with User"""
        item = Item(
            added_by_user_id=user.user_id,
            name="Cafe",
            location="789 Elm St"
        )
        session.add(item)
        session.commit()

        assert item.added_by_user.username == "testuser"
