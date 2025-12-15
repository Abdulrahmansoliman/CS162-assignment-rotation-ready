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
    """Items that can be found/verified in rotation cities.
    
    Each item belongs to categories through the CategoryItem junction table.
    Items are shared by students to help others find useful resources in their city.
    
    Attributes:
        item_id (int): Primary key, auto-incrementing
        added_by_user_id (int): Foreign key to user who added the item
        rotation_city_id (int): Foreign key to rotation_city where item is located
        name (str): Item name (max 200 chars)
        location (str): Physical location description (max 500 chars)
        walking_distance (float): Optional walking distance in meters
        last_verified_date (datetime): When item was last verified as still available
        number_of_verifications (int): Count of user verifications
        created_at (datetime): Item creation timestamp
        added_by_user: Relationship to User who added the item
        rotation_city: Relationship to RotationCity where item is located
        category_items: Relationship to categories through junction table
        item_verifications: Relationship to user verifications of this item
        item_tag_values: Relationship to tag values assigned to this item
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
    rotation_city_id = Column(
        Integer,
        ForeignKey('rotation_city.city_id'),
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
    rotation_city = relationship("RotationCity", back_populates="items")
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
        """Return string representation of Item instance."""
        return (
            f"<Item(item_id={self.item_id}, name='{self.name}', "
            f"location='{self.location}')>"
        )
