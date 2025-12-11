"""
Category Fixtures
"""
import pytest
from app.models import Category


@pytest.fixture
def category(db_session):
    """Create a test category."""
    category = Category(
        category_name='Electronics',
        category_pic='https://example.com/electronics.jpg'
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def furniture_category(db_session):
    """Create a furniture category."""
    category = Category(
        category_name='Furniture',
        category_pic='https://example.com/furniture.jpg'
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def books_category(db_session):
    """Create a books category."""
    category = Category(
        category_name='Books',
        category_pic='https://example.com/books.jpg'
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category
