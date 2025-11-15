"""
Unit tests for Category model
"""
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.db import Base
from app.models.category import Category


class TestCategory(unittest.TestCase):
    """Test cases for Category model"""

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
        self.session.close()

    def test_create_category(self):
        """Test creating a category"""
        category = Category(
            name="Electronics",
            pic="electronics.png"
        )
        self.session.add(category)
        self.session.commit()

        self.assertIsNotNone(category.category_id)
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(category.pic, "electronics.png")

    def test_category_without_pic(self):
        """Test creating category without picture"""
        category = Category(name="Furniture")
        self.session.add(category)
        self.session.commit()

        self.assertIsNotNone(category.category_id)
        self.assertIsNone(category.pic)

    def test_unique_category_name(self):
        """Test that category names must be unique"""
        category1 = Category(name="Books")
        self.session.add(category1)
        self.session.commit()

        category2 = Category(name="Books")
        self.session.add(category2)

        with self.assertRaises(IntegrityError):
            self.session.commit()

    def test_category_id_auto_increment(self):
        """Test that category_id auto-increments"""
        cat1 = Category(name="Sports")
        cat2 = Category(name="Music")
        self.session.add_all([cat1, cat2])
        self.session.commit()

        self.assertNotEqual(cat1.category_id, cat2.category_id)

    def test_repr_method(self):
        """Test string representation"""
        category = Category(name="Food")
        self.session.add(category)
        self.session.commit()

        repr_str = repr(category)
        self.assertIn("Category", repr_str)
        self.assertIn("Food", repr_str)


if __name__ == '__main__':
    unittest.main()
