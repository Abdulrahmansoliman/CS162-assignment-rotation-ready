"""
Unit tests for Value model
"""
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models.value import Value
from app.models.tag import Tag


class TestValue(unittest.TestCase):
    """Test cases for Value model"""

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
        
        self.tag_bool = Tag(
            name="HasParking",
            value_type="boolean"
        )
        self.tag_name = Tag(
            name="Cuisine",
            value_type="name"
        )
        self.tag_num = Tag(
            name="Price",
            value_type="numerical"
        )
        self.session.add_all([self.tag_bool, self.tag_name, self.tag_num])
        self.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        self.session.query(Value).delete()
        self.session.query(Tag).delete()
        self.session.commit()
        self.session.close()

    def test_create_boolean_value(self):
        """Test creating a boolean value"""
        value = Value(
            tag_id=self.tag_bool.tag_id,
            boolean_val=True
        )
        self.session.add(value)
        self.session.commit()

        self.assertIsNotNone(value.value_id)
        self.assertTrue(value.boolean_val)
        self.assertIsNone(value.name_val)
        self.assertIsNone(value.numerical_value)

    def test_create_name_value(self):
        """Test creating a name value"""
        value = Value(
            tag_id=self.tag_name.tag_id,
            name_val="Italian"
        )
        self.session.add(value)
        self.session.commit()

        self.assertIsNotNone(value.value_id)
        self.assertEqual(value.name_val, "Italian")
        self.assertIsNone(value.boolean_val)
        self.assertIsNone(value.numerical_value)

    def test_create_numerical_value(self):
        """Test creating a numerical value"""
        value = Value(
            tag_id=self.tag_num.tag_id,
            numerical_value=25.50
        )
        self.session.add(value)
        self.session.commit()

        self.assertIsNotNone(value.value_id)
        self.assertEqual(value.numerical_value, 25.50)
        self.assertIsNone(value.boolean_val)
        self.assertIsNone(value.name_val)

    def test_relationship_to_tag(self):
        """Test relationship with Tag"""
        value = Value(
            tag_id=self.tag_name.tag_id,
            name_val="Mexican"
        )
        self.session.add(value)
        self.session.commit()

        self.assertEqual(value.tag.name, "Cuisine")
        self.assertEqual(value.tag.value_type, "name")

    def test_value_id_auto_increment(self):
        """Test that value_id auto-increments"""
        val1 = Value(tag_id=self.tag_bool.tag_id, boolean_val=True)
        val2 = Value(tag_id=self.tag_bool.tag_id, boolean_val=False)
        self.session.add_all([val1, val2])
        self.session.commit()

        self.assertNotEqual(val1.value_id, val2.value_id)

    def test_repr_method(self):
        """Test string representation"""
        value = Value(
            tag_id=self.tag_num.tag_id,
            numerical_value=100
        )
        self.session.add(value)
        self.session.commit()

        repr_str = repr(value)
        self.assertIn("Value", repr_str)


if __name__ == '__main__':
    unittest.main()
