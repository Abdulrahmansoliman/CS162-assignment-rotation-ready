"""
Value Model
Possible values for tags. Supports different data types through
separate columns.
"""
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Value(Base):
    """
    Possible values for tags.
    Supports different data types through separate columns
    (boolean, text, numeric).
    """
    __tablename__ = 'value'
    
    # Primary Key with descriptive name
    value_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    tag_id = Column(
        Integer,
        ForeignKey('tag.tag_id'),
        nullable=False
    )
    
    # Value Information (different types stored in different columns)
    boolean_val = Column(Boolean, nullable=True)
    name_val = Column(String(200), nullable=True)  # Text values
    numerical_value = Column(Float, nullable=True)
    
    # Relationships
    tag = relationship("Tag", back_populates="values")
    item_tag_values = relationship(
        "ItemTagValue",
        back_populates="value",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return (
            f"<Value(value_id={self.value_id}, tag_id={self.tag_id}, "
            f"boolean={self.boolean_val}, name='{self.name_val}', "
            f"numeric={self.numerical_value})>"
        )
