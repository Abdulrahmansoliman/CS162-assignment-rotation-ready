"""
Unit tests for Verification model
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import db
from app.models.item_verification import ItemVerification
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
    yield session
    session.query(ItemVerification).delete()
    session.query(Item).delete()
    session.query(User).delete()
    session.query(RotationCity).delete()
    session.commit()
    session.close()


@pytest.fixture
def test_data(session):
    """Create test data"""
    city = RotationCity(name="VerifyCity", time_zone="UTC")
    session.add(city)
    session.commit()
    
    user = User(
        rotation_city_id=city.city_id,
        first_name="Verify",
        last_name="User",
        email="verify@example.com"
    )
    session.add(user)
    session.commit()
    
    item = Item(
        added_by_user_id=user.user_id,
        name="Test Place",
        location="Test Loc"
    )
    session.add(item)
    session.commit()
    
    return {
        'city': city,
        'user': user,
        'item': item
    }


class TestVerification:
    """Test cases for ItemVerification model"""

    def test_create_verification(self, session, test_data):
        """Test creating a verification"""
        verification = ItemVerification(
            user_id=test_data['user'].user_id,
            item_id=test_data['item'].item_id,
            note="Still there!"
        )
        session.add(verification)
        session.commit()

        assert verification.verification_id is not None
        assert verification.user_id == test_data['user'].user_id
        assert verification.item_id == test_data['item'].item_id
        assert verification.note == "Still there!"
        assert isinstance(verification.created_at, datetime)

    def test_verification_without_note(self, session, test_data):
        """Test creating verification without note"""
        verification = ItemVerification(
            user_id=test_data['user'].user_id,
            item_id=test_data['item'].item_id
        )
        session.add(verification)
        session.commit()

        assert verification.note is None

    def test_relationships(self, session, test_data):
        """Test relationships to user and item"""
        verification = ItemVerification(
            user_id=test_data['user'].user_id,
            item_id=test_data['item'].item_id
        )
        session.add(verification)
        session.commit()

        assert verification.user.email == "verify@example.com"
        assert verification.item.name == "Test Place"

    def test_verification_id_auto_increment(self, session, test_data):
        """Test that verification_id auto-increments"""
        ver1 = ItemVerification(
            user_id=test_data['user'].user_id,
            item_id=test_data['item'].item_id
        )
        ver2 = ItemVerification(
            user_id=test_data['user'].user_id,
            item_id=test_data['item'].item_id
        )
        session.add_all([ver1, ver2])
        session.commit()

        assert ver1.verification_id != ver2.verification_id

    def test_timestamp_auto_set(self, session, test_data):
        """Test that created_at is set automatically"""
        verification = ItemVerification(
            user_id=test_data['user'].user_id,
            item_id=test_data['item'].item_id
        )
        session.add(verification)
        session.commit()

        assert verification.created_at is not None
        assert isinstance(verification.created_at, datetime)
