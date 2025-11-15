"""
CategoryItem Model
Junction table linking items to categories (many-to-many relationship).
An item can belong to multiple categories.
"""
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db import Base


class CategoryItem(Base):
    """
    Junction table linking items to categories (many-to-many relationship).
    An item can belong to multiple categories.
    """
    __tablename__ = 'category_item'
    
    # Primary Key with descriptive name
    category_item_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    item_id = Column(
        Integer,
        ForeignKey('item.item_id'),
        nullable=False
    )
    category_id = Column(
        Integer,
        ForeignKey('category.category_id'),
        nullable=False
    )
    
    # Relationships
    item = relationship("Item", back_populates="category_items")
    category = relationship("Category", back_populates="category_items")
    
    def __repr__(self):
        return (
            f"<CategoryItem(category_item_id={self.category_item_id}, "
            f"item_id={self.item_id}, category_id={self.category_id})>"
        )
