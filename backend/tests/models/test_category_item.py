"""
Unit tests for CategoryItem model
"""
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models.category import Category
from app.models.category_item import CategoryItem
from app.models.item import Item
from app.models.user import User
from app.models.rotation_city import RotationCity


class TestCategoryItem(unittest.TestCase):
    """Test cases for CategoryItem junction table"""

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
        
        # Create test data
        self.city = RotationCity(name="TestCity1", time_zone="UTC")
        self.session.add(self.city)
        self.session.commit()
        
        self.user = User(
            rotation_city_id=self.city.city_id,
            first_name="Test",
            last_name="User",
            username="testuser1",
            email="test1@example.com"
        )
        self.session.add(self.user)
        self.session.commit()
        
        self.item = Item(
            added_by_user_id=self.user.user_id,
            name="Test Item",
            location="Test Location"
        )
        self.session.add(self.item)
        self.session.commit()
        
        self.category = Category(name="TestCategory1")
        self.session.add(self.category)
        self.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        self.session.query(CategoryItem).delete()
        self.session.query(Item).delete()
        self.session.query(User).delete()
        self.session.query(Category).delete()
        self.session.query(RotationCity).delete()
        self.session.commit()
        self.session.close()

    def test_create_category_item(self):
        """Test creating a category-item relationship"""
        cat_item = CategoryItem(
            item_id=self.item.item_id,
            category_id=self.category.category_id
        )
        self.session.add(cat_item)
        self.session.commit()

        self.assertIsNotNone(cat_item.category_item_id)
        self.assertEqual(cat_item.item_id, self.item.item_id)
        self.assertEqual(cat_item.category_id, self.category.category_id)

    def test_relationships(self):
        """Test relationships to item and category"""
        cat_item = CategoryItem(
            item_id=self.item.item_id,
            category_id=self.category.category_id
        )
        self.session.add(cat_item)
        self.session.commit()

        self.assertEqual(cat_item.item.name, "Test Item")
        self.assertEqual(cat_item.category.name, "TestCategory1")

    def test_multiple_categories_per_item(self):
        """Test that an item can belong to multiple categories"""
        cat2 = Category(name="TestCategory2")
        self.session.add(cat2)
        self.session.commit()

        cat_item1 = CategoryItem(
            item_id=self.item.item_id,
            category_id=self.category.category_id
        )
        cat_item2 = CategoryItem(
            item_id=self.item.item_id,
            category_id=cat2.category_id
        )
        self.session.add_all([cat_item1, cat_item2])
        self.session.commit()

        self.assertEqual(len(self.item.category_items), 2)


if __name__ == '__main__':
    unittest.main()
