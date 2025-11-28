"""
Unit tests for User model
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import db
from app.models.user import User
from app.models.rotation_city import RotationCity


@pytest.fixture(scope='module')
def engine():
    """Create test database engine"""
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        echo=False
    )
    # Enable foreign key constraints for SQLite
    from sqlalchemy import event

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
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
def rotation_city(session):
    """Create a test rotation city"""
    city = RotationCity(
        name="Test City",
        time_zone="UTC"
    )
    session.add(city)
    session.commit()
    return city


class TestUser:
    """Test cases for User model"""

    def test_create_user(self, session, rotation_city):
        """Test creating a user"""
        user = User(
            rotation_city_id=rotation_city.city_id,
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        session.add(user)
        session.commit()

        assert user.user_id is not None
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john@example.com"

    def test_user_id_auto_increment(self, session, rotation_city):
        """Test that user_id auto-increments"""
        user1 = User(
            rotation_city_id=rotation_city.city_id,
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com"
        )
        user2 = User(
            rotation_city_id=rotation_city.city_id,
            first_name="Bob",
            last_name="Jones",
            email="bob@example.com"
        )
        session.add_all([user1, user2])
        session.commit()

        assert user1.user_id != user2.user_id



    def test_unique_email(self, session, rotation_city):
        """Test that emails must be unique"""
        user1 = User(
            rotation_city_id=rotation_city.city_id,
            first_name="User",
            last_name="One",
            email="test@example.com"
        )
        session.add(user1)
        session.commit()

        session.rollback()

        user2 = User(
            rotation_city_id=rotation_city.city_id,
            first_name="User",
            last_name="Two",
            email="test@example.com"
        )
        session.add(user2)

        with pytest.raises(Exception):
            session.commit()

    def test_timestamps(self, session, rotation_city):
        """Test that timestamps are set automatically"""
        user = User(
            rotation_city_id=rotation_city.city_id,
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com"
        )
        session.add(user)
        session.commit()

        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_foreign_key_constraint(self, session):
        """Test that rotation_city_id must be valid"""
        user = User(
            rotation_city_id=9999,
            first_name="Test",
            last_name="User",
            email="testfk@example.com"
        )
        session.add(user)

        with pytest.raises(Exception):
            session.commit()

    def test_relationship_to_city(self, session, rotation_city):
        """Test relationship with RotationCity"""
        user = User(
            rotation_city_id=rotation_city.city_id,
            first_name="Test",
            last_name="User",
            email="testrel@example.com"
        )
        session.add(user)
        session.commit()

        assert user.rotation_city.name == "Test City"
