"""
Models Package
Imports all database models for easy access.
"""
from app.db import Base, engine

# Import all models
from app.models.rotation_city import RotationCity
from app.models.user import User
from app.models.category import Category
from app.models.item import Item
from app.models.category_item import CategoryItem
from app.models.verification import Verification
from app.models.tag import Tag
from app.models.value import Value
from app.models.item_tag_value import ItemTagValue

# Export all models
__all__ = [
    'Base',
    'engine',
    'RotationCity',
    'User',
    'Category',
    'Item',
    'CategoryItem',
    'Verification',
    'Tag',
    'Value',
    'ItemTagValue',
]


def create_all_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def drop_all_tables():
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)

