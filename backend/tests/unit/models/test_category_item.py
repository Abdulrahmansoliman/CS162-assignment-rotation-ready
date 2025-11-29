"""
Unit tests for CategoryItem model
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import db
from app.models.category import Category
from app.models.category_item import CategoryItem
from app.models.item import Item
from app.models.user import User
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
    session.query(CategoryItem).delete()
    session.query(Item).delete()
    session.query(User).delete()
    session.query(Category).delete()
    session.query(RotationCity).delete()
    session.commit()
    session.close()


@pytest.fixture
def test_data(session):
    """Create test data"""
    city = RotationCity(name="TestCity1", time_zone="UTC")
    session.add(city)
    session.commit()
    
    user = User(
        rotation_city_id=city.city_id,
        first_name="Test",
        last_name="User",
        email="test1@example.com"
    )
    session.add(user)
    session.commit()
    
    item = Item(
        added_by_user_id=user.user_id,
        rotation_city_id=city.city_id,
        name="Test Item",
        location="Test Location"
    )
    session.add(item)
    session.commit()
    
    category = Category(name="TestCategory1")
    session.add(category)
    session.commit()
    
    return {
        'city': city,
        'user': user,
        'item': item,
        'category': category
    }


class TestCategoryItem:
    """Test cases for CategoryItem junction table"""

    def test_create_category_item(self, session, test_data):
        """Test creating a category-item relationship"""
        cat_item = CategoryItem(
            item_id=test_data['item'].item_id,
            category_id=test_data['category'].category_id
        )
        session.add(cat_item)
        session.commit()

        assert cat_item.category_item_id is not None
        assert cat_item.item_id == test_data['item'].item_id
        assert cat_item.category_id == test_data['category'].category_id

    def test_relationships(self, session, test_data):
        """Test relationships to item and category"""
        cat_item = CategoryItem(
            item_id=test_data['item'].item_id,
            category_id=test_data['category'].category_id
        )
        session.add(cat_item)
        session.commit()

        assert cat_item.item.name == "Test Item"
        assert cat_item.category.name == "TestCategory1"

    def test_multiple_categories_per_item(self, session, test_data):
        """Test that an item can belong to multiple categories"""
        cat2 = Category(name="TestCategory2")
        session.add(cat2)
        session.commit()

        cat_item1 = CategoryItem(
            item_id=test_data['item'].item_id,
            category_id=test_data['category'].category_id
        )
        cat_item2 = CategoryItem(
            item_id=test_data['item'].item_id,
            category_id=cat2.category_id
        )
        session.add_all([cat_item1, cat_item2])
        session.commit()

        assert len(test_data['item'].category_items) == 2
