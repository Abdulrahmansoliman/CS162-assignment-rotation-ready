"""
Item Model
Items that can be found/verified in rotation cities.
Each item belongs to categories through the junction table.
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app import db


class Item(db.Model):
    """
    Items that can be found/verified in rotation cities.
    Each item belongs to categories through the CategoryItem junction table.
    """
    __tablename__ = 'item'
    
    # Primary Key with descriptive name
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    added_by_user_id = Column(
        Integer,
        ForeignKey('user.user_id'),
        nullable=False
    )
    
    # Item Information
    name = Column(String(200), nullable=False)
    location = Column(String(500), nullable=False)
    walking_distance = Column(Float, nullable=True)
    last_verified_date = Column(DateTime, nullable=True)
    number_of_verifications = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    added_by_user = relationship("User", back_populates="added_items")
    category_items = relationship(
        "CategoryItem",
        back_populates="item",
        cascade="all, delete-orphan"
    )
    item_verifications = relationship(
        "ItemVerification",
        back_populates="item",
        cascade="all, delete-orphan"
    )
    item_tag_values = relationship(
        "ItemTagValue",
        back_populates="item",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return (
            f"<Item(item_id={self.item_id}, name='{self.name}', "
            f"location='{self.location}')>"
        )
