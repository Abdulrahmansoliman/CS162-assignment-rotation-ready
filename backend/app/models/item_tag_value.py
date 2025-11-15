"""
ItemTagValue Model
Junction table linking items to specific tag values.
Associates items with their tag metadata.
"""
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db import Base


class ItemTagValue(Base):
    """
    Junction table linking items to specific tag values.
    Associates items with their tag metadata.
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
        return (
            f"<ItemTagValue(item_tag_value_id={self.item_tag_value_id}, "
            f"item_id={self.item_id}, value_id={self.value_id})>"
        )
