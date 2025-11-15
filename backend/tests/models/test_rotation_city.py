"""
Unit tests for RotationCity model
"""
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models.rotation_city import RotationCity


class TestRotationCity(unittest.TestCase):
    """Test cases for RotationCity model"""

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

    def test_create_rotation_city(self):
        """Test creating a rotation city"""
        city = RotationCity(
            name="San Francisco",
            time_zone="America/Los_Angeles",
            res_hall_location="123 Main St"
        )
        self.session.add(city)
        self.session.commit()

        self.assertIsNotNone(city.city_id)
        self.assertEqual(city.name, "San Francisco")
        self.assertEqual(city.time_zone, "America/Los_Angeles")
        self.assertEqual(city.res_hall_location, "123 Main St")

    def test_city_id_auto_increment(self):
        """Test that city_id auto-increments"""
        city1 = RotationCity(
            name="Berlin",
            time_zone="Europe/Berlin"
        )
        city2 = RotationCity(
            name="Seoul",
            time_zone="Asia/Seoul"
        )
        self.session.add_all([city1, city2])
        self.session.commit()

        self.assertIsNotNone(city1.city_id)
        self.assertIsNotNone(city2.city_id)
        self.assertNotEqual(city1.city_id, city2.city_id)

    def test_unique_city_name(self):
        """Test that city names must be unique"""
        city1 = RotationCity(
            name="London",
            time_zone="Europe/London"
        )
        self.session.add(city1)
        self.session.commit()

        city2 = RotationCity(
            name="London",
            time_zone="Europe/London"
        )
        self.session.add(city2)

        with self.assertRaises(Exception):
            self.session.commit()

    def test_required_fields(self):
        """Test that required fields cannot be null"""
        city = RotationCity(time_zone="America/New_York")
        self.session.add(city)

        with self.assertRaises(Exception):
            self.session.commit()

    def test_optional_res_hall_location(self):
        """Test that res_hall_location is optional"""
        city = RotationCity(
            name="Tokyo",
            time_zone="Asia/Tokyo"
        )
        self.session.add(city)
        self.session.commit()

        self.assertIsNone(city.res_hall_location)

    def test_repr_method(self):
        """Test string representation"""
        city = RotationCity(
            name="Buenos Aires",
            time_zone="America/Argentina/Buenos_Aires"
        )
        self.session.add(city)
        self.session.commit()

        repr_str = repr(city)
        self.assertIn("RotationCity", repr_str)
        self.assertIn(str(city.city_id), repr_str)
        self.assertIn("Buenos Aires", repr_str)


if __name__ == '__main__':
    unittest.main()
