"""
Unit tests for Category model
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.category import Category


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


class TestCategory:
    """Test cases for Category model"""

    def test_create_category(self, session):
        """Test creating a category"""
        category = Category(
            category_name="Electronics",
            category_pic="electronics.png"
        )
        session.add(category)
        session.commit()

        assert category.category_id is not None
        assert category.category_name == "Electronics"
        assert category.category_pic == "electronics.png"

    def test_category_without_pic(self, session):
        """Test creating category without picture"""
        category = Category(category_name="Furniture")
        session.add(category)
        session.commit()

        assert category.category_id is not None
        assert category.category_pic is None

    def test_unique_category_name(self, session):
        """Test that category names must be unique"""
        category1 = Category(category_name="Books")
        session.add(category1)
        session.commit()

        category2 = Category(category_name="Books")
        session.add(category2)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_category_id_auto_increment(self, session):
        """Test that category_id auto-increments"""
        cat1 = Category(category_name="Sports")
        cat2 = Category(category_name="Music")
        session.add_all([cat1, cat2])
        session.commit()

        assert cat1.category_id != cat2.category_id

    def test_repr_method(self, session):
        """Test string representation"""
        category = Category(category_name="Food")
        session.add(category)
        session.commit()

        repr_str = repr(category)
        assert "Category" in repr_str
        assert "Food" in repr_str
