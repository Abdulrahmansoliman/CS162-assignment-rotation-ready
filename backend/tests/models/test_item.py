"""
Unit tests for Item model
"""
import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models.item import Item
from app.models.user import User
from app.models.rotation_city import RotationCity


class TestItem(unittest.TestCase):
    """Test cases for Item model"""

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
        # Clear all tables before each test
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()
        
        self.city = RotationCity(
            name="Test City",
            time_zone="UTC"
        )
        self.session.add(self.city)
        self.session.commit()
        
        self.user = User(
            rotation_city_id=self.city.city_id,
            first_name="Test",
            last_name="User",
            username="testuser",
            email="test@example.com"
        )
        self.session.add(self.user)
        self.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        self.session.rollback()
        self.session.close()

    def test_create_item(self):
        """Test creating an item"""
        item = Item(
            added_by_user_id=self.user.user_id,
            name="Grocery Store",
            location="123 Main St",
            walking_distance=5.5
        )
        self.session.add(item)
        self.session.commit()

        self.assertIsNotNone(item.item_id)
        self.assertEqual(item.name, "Grocery Store")
        self.assertEqual(item.location, "123 Main St")
        self.assertEqual(item.walking_distance, 5.5)

    def test_item_defaults(self):
        """Test default values for item"""
        item = Item(
            added_by_user_id=self.user.user_id,
            name="Library",
            location="456 Oak Ave"
        )
        self.session.add(item)
        self.session.commit()

        self.assertEqual(item.number_of_verifications, 0)
        self.assertIsNone(item.last_verified_date)
        self.assertIsInstance(item.created_at, datetime)

    def test_relationship_to_user(self):
        """Test relationship with User"""
        item = Item(
            added_by_user_id=self.user.user_id,
            name="Cafe",
            location="789 Elm St"
        )
        self.session.add(item)
        self.session.commit()

        self.assertEqual(item.added_by_user.username, "testuser")


if __name__ == '__main__':
    unittest.main()
