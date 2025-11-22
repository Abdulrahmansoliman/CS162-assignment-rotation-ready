"""
Unit tests for Verification model
"""
import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models.verification import Verification
from app.models.item import Item
from app.models.user import User
from app.models.rotation_city import RotationCity


class TestVerification(unittest.TestCase):
    """Test cases for Verification model"""

    @classmethod
    def setUpClass(cls):
        """Set up test database once for all tests"""
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def setUp(self):
        """Set up before each test"""
        self.session = self.Session()
        
        self.city = RotationCity(name="VerifyCity", time_zone="UTC")
        self.session.add(self.city)
        self.session.commit()
        
        self.user = User(
            rotation_city_id=self.city.city_id,
            first_name="Verify",
            last_name="User",
            username="verifyuser",
            email="verify@example.com"
        )
        self.session.add(self.user)
        self.session.commit()
        
        self.item = Item(
            added_by_user_id=self.user.user_id,
            name="Test Place",
            location="Test Loc"
        )
        self.session.add(self.item)
        self.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        self.session.query(Verification).delete()
        self.session.query(Item).delete()
        self.session.query(User).delete()
        self.session.query(RotationCity).delete()
        self.session.commit()
        self.session.close()

    def test_create_verification(self):
        """Test creating a verification"""
        verification = Verification(
            user_id=self.user.user_id,
            item_id=self.item.item_id,
            note="Still there!"
        )
        self.session.add(verification)
        self.session.commit()

        self.assertIsNotNone(verification.verification_id)
        self.assertEqual(verification.user_id, self.user.user_id)
        self.assertEqual(verification.item_id, self.item.item_id)
        self.assertEqual(verification.note, "Still there!")
        self.assertIsInstance(verification.created_at, datetime)

    def test_verification_without_note(self):
        """Test creating verification without note"""
        verification = Verification(
            user_id=self.user.user_id,
            item_id=self.item.item_id
        )
        self.session.add(verification)
        self.session.commit()

        self.assertIsNone(verification.note)

    def test_relationships(self):
        """Test relationships to user and item"""
        verification = Verification(
            user_id=self.user.user_id,
            item_id=self.item.item_id
        )
        self.session.add(verification)
        self.session.commit()

        self.assertEqual(verification.user.username, "verifyuser")
        self.assertEqual(verification.item.name, "Test Place")

    def test_verification_id_auto_increment(self):
        """Test that verification_id auto-increments"""
        ver1 = Verification(
            user_id=self.user.user_id,
            item_id=self.item.item_id
        )
        ver2 = Verification(
            user_id=self.user.user_id,
            item_id=self.item.item_id
        )
        self.session.add_all([ver1, ver2])
        self.session.commit()

        self.assertNotEqual(ver1.verification_id, ver2.verification_id)

    def test_timestamp_auto_set(self):
        """Test that created_at is set automatically"""
        verification = Verification(
            user_id=self.user.user_id,
            item_id=self.item.item_id
        )
        self.session.add(verification)
        self.session.commit()

        self.assertIsNotNone(verification.created_at)
        self.assertIsInstance(verification.created_at, datetime)


if __name__ == '__main__':
    unittest.main()
