"""
Verification Model
Records when users verify that an item still exists/is available.
Helps keep item information current.
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app import db


class ItemVerification(db.Model):
    """Records when users verify that an item still exists/is available.
    
    Helps keep item information current and reliable by tracking
    user confirmations that items are still accessible.
    
    Attributes:
        verification_id (int): Primary key, auto-incrementing
        user_id (int): Foreign key to user who verified the item
        item_id (int): Foreign key to item being verified
        note (str): Optional text note from verifier
        created_at (datetime): Verification timestamp
        user: Relationship to User model
        item: Relationship to Item model
    """
    __tablename__ = 'item_verification'
    
    # Primary Key with descriptive name
    verification_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    user_id = Column(
        Integer,
        ForeignKey('user.user_id'),
        nullable=False
    )
    item_id = Column(
        Integer,
        ForeignKey('item.item_id'),
        nullable=False
    )
    
    # Verification Information
    note = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="item_verifications")
    item = relationship("Item", back_populates="item_verifications")
    
    def __repr__(self):
        """Return string representation of ItemVerification instance."""
        return (
            f"<ItemVerification(verification_id={self.verification_id}, "
            f"user_id={self.user_id}, item_id={self.item_id})>"
        )
