"""
Tag Model
Tags that can be applied to items for additional metadata.
Supports different value types (boolean, text, numeric).
"""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app import db


"""
Enum definitions for database models.
Uses integer values for database storage with mapped labels.
"""
from enum import Enum


class TagValueType(Enum):
    """Enum for tag value types."""
    BOOLEAN = (0, "boolean")
    TEXT = (1, "text")
    NUMERIC = (2, "numeric")

    def __init__(self, code, label):
        self._code = code
        self._label = label

    @property
    def code(self):
        return self._code

    @property
    def label(self):
        return self._label

    @classmethod
    def from_code(cls, code):
        """Get enum member from code value."""
        for member in cls:
            if member.code == code:
                return member
        raise ValueError(f"Invalid TagValueType code: {code}")

    @classmethod
    def from_label(cls, label):
        """Get enum member from label string."""
        for member in cls:
            if member.label == label:
                return member
        raise ValueError(f"Invalid TagValueType label: {label}")
    

class Tag(db.Model):
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
        Integer,
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

    @property
    def value_type_enum(self):
        """Get the TagValueType enum for this tag's value_type code."""
        return TagValueType.from_code(self.value_type)

    @property
    def value_type_label(self):
        """Get the human-readable label for this tag's value_type."""
        return self.value_type_enum.label
    
    def __repr__(self):
        return (
            f"<Tag(tag_id={self.tag_id}, name='{self.name}', "
            f"value_type='{self.value_type_label}')>"
        )
