"""
Value Model
Possible values for tags. Supports different data types through
separate columns.
"""
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app import db


class Value(db.Model):
    """Possible values for tags.
    
    Supports different data types through separate columns.
    Only one column (boolean_val, name_val, or numerical_value) should be set
    per value instance, determined by the associated tag's value_type.
    
    Attributes:
        value_id (int): Primary key, auto-incrementing
        tag_id (int): Foreign key to tag this value belongs to
        boolean_val (bool): Boolean value (for BOOLEAN tags)
        name_val (str): Text value (for TEXT tags, max 200 chars)
        numerical_value (float): Numeric value (for NUMERIC tags)
        tag: Relationship to Tag model
        item_tag_values: Relationship to items using this value
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
        """Return string representation of Value instance."""
        return (
            f"<Value(value_id={self.value_id}, tag_id={self.tag_id}, "
            f"boolean={self.boolean_val}, name='{self.name_val}', "
            f"numeric={self.numerical_value})>"
        )
