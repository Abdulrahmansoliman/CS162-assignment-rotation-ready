"""
Tag Model
Tags that can be applied to items for additional metadata.
Supports different value types (boolean, text, numeric).
"""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Tag(Base):
    """
    Tags that can be applied to items for additional metadata.
    Supports different value types (boolean, text, numeric).
    """
    __tablename__ = 'tag'
    
    # Primary Key with descriptive name
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Tag Information
    name = Column(String(100), nullable=False, unique=True)
    value_type = Column(
        String(20),
        nullable=False
    )  # 'boolean', 'text', 'numeric'
    can_add_new_value = Column(
        Boolean,
        default=True
    )  # Whether users can add custom values
    
    # Relationships
    values = relationship(
        "Value",
        back_populates="tag",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return (
            f"<Tag(tag_id={self.tag_id}, name='{self.name}', "
            f"value_type='{self.value_type}')>"
        )
