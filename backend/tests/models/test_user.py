"""
Unit tests for User model
"""
import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models.user import User
from app.models.rotation_city import RotationCity


class TestUser(unittest.TestCase):
    """Test cases for User model"""

    @classmethod
    def setUpClass(cls):
        """Set up test database once for all tests"""
        cls.engine = create_engine(
            'sqlite:///:memory:',
            connect_args={'check_same_thread': False},
            echo=False
        )
        # Enable foreign key constraints for SQLite
        from sqlalchemy import event

        @event.listens_for(cls.engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        
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

    def tearDown(self):
        """Clean up after each test"""
        self.session.rollback()
        self.session.close()

    def test_create_user(self):
        """Test creating a user"""
        user = User(
            rotation_city_id=self.city.city_id,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john@example.com"
        )
        self.session.add(user)
        self.session.commit()

        self.assertIsNotNone(user.user_id)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.username, "johndoe")
        self.assertEqual(user.email, "john@example.com")

    def test_user_id_auto_increment(self):
        """Test that user_id auto-increments"""
        user1 = User(
            rotation_city_id=self.city.city_id,
            first_name="Alice",
            last_name="Smith",
            username="alice",
            email="alice@example.com"
        )
        user2 = User(
            rotation_city_id=self.city.city_id,
            first_name="Bob",
            last_name="Jones",
            username="bob",
            email="bob@example.com"
        )
        self.session.add_all([user1, user2])
        self.session.commit()

        self.assertNotEqual(user1.user_id, user2.user_id)

    def test_unique_username(self):
        """Test that usernames must be unique"""
        user1 = User(
            rotation_city_id=self.city.city_id,
            first_name="User",
            last_name="One",
            username="testuser",
            email="user1@example.com"
        )
        self.session.add(user1)
        self.session.commit()

        user2 = User(
            rotation_city_id=self.city.city_id,
            first_name="User",
            last_name="Two",
            username="testuser",
            email="user2@example.com"
        )
        self.session.add(user2)

        with self.assertRaises(Exception):
            self.session.commit()

    def test_unique_email(self):
        """Test that emails must be unique"""
        user1 = User(
            rotation_city_id=self.city.city_id,
            first_name="User",
            last_name="One",
            username="user1",
            email="test@example.com"
        )
        self.session.add(user1)
        self.session.commit()

        self.session.rollback()

        user2 = User(
            rotation_city_id=self.city.city_id,
            first_name="User",
            last_name="Two",
            username="user2",
            email="test@example.com"
        )
        self.session.add(user2)

        with self.assertRaises(Exception):
            self.session.commit()

    def test_timestamps(self):
        """Test that timestamps are set automatically"""
        user = User(
            rotation_city_id=self.city.city_id,
            first_name="Jane",
            last_name="Doe",
            username="janedoe",
            email="jane@example.com"
        )
        self.session.add(user)
        self.session.commit()

        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)

    def test_foreign_key_constraint(self):
        """Test that rotation_city_id must be valid"""
        user = User(
            rotation_city_id=9999,
            first_name="Test",
            last_name="User",
            username="testfk",
            email="testfk@example.com"
        )
        self.session.add(user)

        with self.assertRaises(Exception):
            self.session.commit()

    def test_relationship_to_city(self):
        """Test relationship with RotationCity"""
        user = User(
            rotation_city_id=self.city.city_id,
            first_name="Test",
            last_name="User",
            username="testrel",
            email="testrel@example.com"
        )
        self.session.add(user)
        self.session.commit()

        self.assertEqual(user.rotation_city.name, "Test City")


if __name__ == '__main__':
    unittest.main()
