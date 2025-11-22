"""
Item and Category Fixtures
"""
import pytest
from app.models import Item, Category, CategoryItem


@pytest.fixture
def category(db_session):
    """Create a test category."""
    category = Category(
        name='Electronics',
        pic='https://example.com/electronics.jpg'
    )
    db_session.add(category)
    db_session.commit()
    return category


@pytest.fixture
def furniture_category(db_session):
    """Create a furniture category."""
    category = Category(
        name='Furniture',
        pic='https://example.com/furniture.jpg'
    )
    db_session.add(category)
    db_session.commit()
    return category


@pytest.fixture
def item(db_session, user, category):
    """Create a test item with category."""
    item = Item(
        name='Laptop',
        location='Library Floor 2',
        walking_distance=150.5,
        added_by_user_id=user.user_id,
        number_of_verifications=0
    )
    db_session.add(item)
    db_session.flush()
    
    # Add to category
    category_item = CategoryItem(
        item_id=item.item_id,
        category_id=category.category_id
    )
    db_session.add(category_item)
    db_session.commit()
    return item


@pytest.fixture
def book(db_session, user, category):
    """Create a book item."""
    item = Item(
        name='Introduction to Algorithms',
        location='Science Building',
        walking_distance=200.0,
        added_by_user_id=user.user_id,
        number_of_verifications=0
    )
    db_session.add(item)
    db_session.flush()
    
    category_item = CategoryItem(
        item_id=item.item_id,
        category_id=category.category_id
    )
    db_session.add(category_item)
    db_session.commit()
    return item
