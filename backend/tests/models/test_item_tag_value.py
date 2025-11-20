"""
Unit tests for ItemTagValue model
"""
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models.item_tag_value import ItemTagValue
from app.models.item import Item
from app.models.tag import Tag
from app.models.value import Value
from app.models.user import User
from app.models.rotation_city import RotationCity


class TestItemTagValue(unittest.TestCase):
    """Test cases for ItemTagValue junction table"""

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
        
        # Create city, user, and item
        self.city = RotationCity(name="TagCity", time_zone="UTC")
        self.session.add(self.city)
        self.session.commit()
        
        self.user = User(
            rotation_city_id=self.city.city_id,
            first_name="Tag",
            last_name="User",
            username="taguser",
            email="tag@example.com"
        )
        self.session.add(self.user)
        self.session.commit()
        
        self.item = Item(
            added_by_user_id=self.user.user_id,
            name="Restaurant",
            location="Downtown"
        )
        self.session.add(self.item)
        self.session.commit()
        
        # Create tag and value
        self.tag = Tag(name="Rating", value_type="numerical")
        self.session.add(self.tag)
        self.session.commit()
        
        self.value = Value(
            tag_id=self.tag.tag_id,
            numerical_value=4.5
        )
        self.session.add(self.value)
        self.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        self.session.query(ItemTagValue).delete()
        self.session.query(Value).delete()
        self.session.query(Tag).delete()
        self.session.query(Item).delete()
        self.session.query(User).delete()
        self.session.query(RotationCity).delete()
        self.session.commit()
        self.session.close()

    def test_create_item_tag_value(self):
        """Test creating an item-tag-value relationship"""
        itv = ItemTagValue(
            item_id=self.item.item_id,
            value_id=self.value.value_id
        )
        self.session.add(itv)
        self.session.commit()

        self.assertIsNotNone(itv.item_tag_value_id)
        self.assertEqual(itv.item_id, self.item.item_id)
        self.assertEqual(itv.value_id, self.value.value_id)

    def test_relationships(self):
        """Test relationships to item and value"""
        itv = ItemTagValue(
            item_id=self.item.item_id,
            value_id=self.value.value_id
        )
        self.session.add(itv)
        self.session.commit()

        self.assertEqual(itv.item.name, "Restaurant")
        self.assertEqual(itv.value.numerical_value, 4.5)

    def test_multiple_tags_per_item(self):
        """Test that an item can have multiple tag-value pairs"""
        # Create another tag and value
        tag2 = Tag(name="PriceRange", value_type="name")
        self.session.add(tag2)
        self.session.commit()
        
        value2 = Value(tag_id=tag2.tag_id, name_val="$$")
        self.session.add(value2)
        self.session.commit()
        
        # Create two item-tag-value relationships
        itv1 = ItemTagValue(
            item_id=self.item.item_id,
            value_id=self.value.value_id
        )
        itv2 = ItemTagValue(
            item_id=self.item.item_id,
            value_id=value2.value_id
        )
        self.session.add_all([itv1, itv2])
        self.session.commit()

        item_tag_values = self.session.query(ItemTagValue).filter_by(
            item_id=self.item.item_id
        ).all()
        self.assertEqual(len(item_tag_values), 2)

    def test_item_tag_value_id_auto_increment(self):
        """Test that item_tag_value_id auto-increments"""
        # Create another value
        value2 = Value(tag_id=self.tag.tag_id, numerical_value=5.0)
        self.session.add(value2)
        self.session.commit()
        
        itv1 = ItemTagValue(
            item_id=self.item.item_id,
            value_id=self.value.value_id
        )
        itv2 = ItemTagValue(
            item_id=self.item.item_id,
            value_id=value2.value_id
        )
        self.session.add_all([itv1, itv2])
        self.session.commit()

        self.assertNotEqual(
            itv1.item_tag_value_id,
            itv2.item_tag_value_id
        )


if __name__ == '__main__':
    unittest.main()
