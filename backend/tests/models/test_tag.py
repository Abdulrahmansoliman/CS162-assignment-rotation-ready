"""
Unit tests for Tag model
"""
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.db import Base
from app.models.tag import Tag


class TestTag(unittest.TestCase):
    """Test cases for Tag model"""

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

    def tearDown(self):
        """Clean up after each test"""
        self.session.rollback()
        self.session.query(Tag).delete()
        self.session.commit()
        self.session.close()

    def test_create_tag(self):
        """Test creating a tag"""
        tag = Tag(
            name="Price",
            value_type="numerical",
            can_add_new_value=True
        )
        self.session.add(tag)
        self.session.commit()

        self.assertIsNotNone(tag.tag_id)
        self.assertEqual(tag.name, "Price")
        self.assertEqual(tag.value_type, "numerical")
        self.assertTrue(tag.can_add_new_value)

    def test_tag_with_boolean_type(self):
        """Test creating tag with boolean value type"""
        tag = Tag(
            name="Is Open",
            value_type="boolean",
            can_add_new_value=False
        )
        self.session.add(tag)
        self.session.commit()

        self.assertEqual(tag.value_type, "boolean")
        self.assertFalse(tag.can_add_new_value)

    def test_tag_with_name_type(self):
        """Test creating tag with name value type"""
        tag = Tag(
            name="Color",
            value_type="name",
            can_add_new_value=True
        )
        self.session.add(tag)
        self.session.commit()

        self.assertEqual(tag.value_type, "name")

    def test_unique_tag_name(self):
        """Test that tag names must be unique"""
        tag1 = Tag(name="Hours", value_type="name")
        self.session.add(tag1)
        self.session.commit()

        tag2 = Tag(name="Hours", value_type="numerical")
        self.session.add(tag2)

        with self.assertRaises(IntegrityError):
            self.session.commit()

    def test_tag_id_auto_increment(self):
        """Test that tag_id auto-increments"""
        tag1 = Tag(name="Rating", value_type="numerical")
        tag2 = Tag(name="Status", value_type="name")
        self.session.add_all([tag1, tag2])
        self.session.commit()

        self.assertNotEqual(tag1.tag_id, tag2.tag_id)

    def test_repr_method(self):
        """Test string representation"""
        tag = Tag(name="WiFi", value_type="boolean")
        self.session.add(tag)
        self.session.commit()

        repr_str = repr(tag)
        self.assertIn("Tag", repr_str)
        self.assertIn("WiFi", repr_str)


if __name__ == '__main__':
    unittest.main()
