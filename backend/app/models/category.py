"""
Category Model
Categories for organizing items (e.g., Electronics, Furniture, etc.)
"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app import db


class Category(db.Model):
    """
    Categories for organizing items.
    Items can belong to multiple categories through the CategoryItem
    junction table.
    """
    __tablename__ = 'category'
    
    # Primary Key with descriptive name
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Category Information
    category_name = Column(String(100), nullable=False, unique=True)
    category_pic = Column(Text, nullable=True)  # Base64 encoded image data
    
    # Relationships
    category_items = relationship(
        "CategoryItem",
        back_populates="category",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return (
            f"<Category(category_id={self.category_id}, "
            f"category_name='{self.category_name}')>"
        )
