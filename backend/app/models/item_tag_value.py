"""
ItemTagValue Model
Junction table linking items to specific tag values.
Associates items with their tag metadata.
"""
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app import db


class ItemTagValue(db.Model):
    """Junction table linking items to specific tag values.
    
    Associates items with their tag metadata (e.g., item has WiFi=true).
    This links an item to a specific value from the value table,
    which in turn references a tag.
    
    Attributes:
        item_tag_value_id (int): Primary key, auto-incrementing
        item_id (int): Foreign key to item table
        value_id (int): Foreign key to value table
        item: Relationship to Item model
        value: Relationship to Value model (which links to Tag)
    """
    __tablename__ = 'item_tag_value'
    
    # Primary Key with descriptive name
    item_tag_value_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    item_id = Column(
        Integer,
        ForeignKey('item.item_id'),
        nullable=False
    )
    value_id = Column(
        Integer,
        ForeignKey('value.value_id'),
        nullable=False
    )
    
    # Relationships
    item = relationship("Item", back_populates="item_tag_values")
    value = relationship("Value", back_populates="item_tag_values")
    
    def __repr__(self):
        """Return string representation of ItemTagValue instance."""
        return (
            f"<ItemTagValue(item_tag_value_id={self.item_tag_value_id}, "
            f"item_id={self.item_id}, value_id={self.value_id})>"
        )
