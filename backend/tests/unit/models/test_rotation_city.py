"""
Unit tests for RotationCity model
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import db
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
    session.rollback()
    session.close()


class TestRotationCity:
    """Test cases for RotationCity model"""

    def test_create_rotation_city(self, session):
        """Test creating a rotation city"""
        city = RotationCity(
            name="San Francisco",
            time_zone="America/Los_Angeles",
            res_hall_location="123 Main St"
        )
        session.add(city)
        session.commit()

        assert city.city_id is not None
        assert city.name == "San Francisco"
        assert city.time_zone == "America/Los_Angeles"
        assert city.res_hall_location == "123 Main St"

    def test_city_id_auto_increment(self, session):
        """Test that city_id auto-increments"""
        city1 = RotationCity(
            name="Berlin",
            time_zone="Europe/Berlin"
        )
        city2 = RotationCity(
            name="Seoul",
            time_zone="Asia/Seoul"
        )
        session.add_all([city1, city2])
        session.commit()

        assert city1.city_id is not None
        assert city2.city_id is not None
        assert city1.city_id != city2.city_id

    def test_unique_city_name(self, session):
        """Test that city names must be unique"""
        city1 = RotationCity(
            name="London",
            time_zone="Europe/London"
        )
        session.add(city1)
        session.commit()

        city2 = RotationCity(
            name="London",
            time_zone="Europe/London"
        )
        session.add(city2)

        with pytest.raises(Exception):
            session.commit()

    def test_required_fields(self, session):
        """Test that required fields cannot be null"""
        city = RotationCity(time_zone="America/New_York")
        session.add(city)

        with pytest.raises(Exception):
            session.commit()

    def test_optional_res_hall_location(self, session):
        """Test that res_hall_location is optional"""
        city = RotationCity(
            name="Tokyo",
            time_zone="Asia/Tokyo"
        )
        session.add(city)
        session.commit()

        assert city.res_hall_location is None

    def test_repr_method(self, session):
        """Test string representation"""
        city = RotationCity(
            name="Buenos Aires",
            time_zone="America/Argentina/Buenos_Aires"
        )
        session.add(city)
        session.commit()

        repr_str = repr(city)
        assert "RotationCity" in repr_str
        assert str(city.city_id) in repr_str
        assert "Buenos Aires" in repr_str
