"""
User Model
Represents a user in the system. Each user belongs to a rotation city
and can add/verify items.
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.verification_stutus_enum import VerificationStatusEnum

from app import db


class User(db.Model):
    """Represents a user in the system.
    
    Each user belongs to a rotation city and can add/verify items.
    Users must verify their email before gaining full access.
    
    Attributes:
        user_id (int): Primary key, auto-incrementing
        rotation_city_id (int): Foreign key to rotation_city
        first_name (str): User's first name (max 50 chars)
        last_name (str): User's last name (max 50 chars)
        email (str): Unique email address (max 100 chars)
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last update timestamp
        is_verified (bool): Email verification status
        status (int): Verification status code (PENDING/VERIFIED)
        rotation_city: Relationship to RotationCity model
        added_items: Relationship to items added by this user
        item_verifications: Relationship to item verifications by this user
        verification_codes: Relationship to verification codes for this user
    """
    __tablename__ = "user"
    
    # Primary Key with descriptive name
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    rotation_city_id = Column(
        Integer,
        ForeignKey('rotation_city.city_id'),
        nullable=False
    )
    
    # User Information
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Account Verification Status
    is_verified = Column(Boolean, default=False, nullable=False, index=True)
    status = Column(
        Integer,
        nullable=False,
        default=VerificationStatusEnum.PENDING.code
    )
    
    # Relationships
    rotation_city = relationship("RotationCity", back_populates="users")
    added_items = relationship("Item", back_populates="added_by_user")
    item_verifications = relationship("ItemVerification", back_populates="user")
    verification_codes = relationship("VerificationCode", back_populates="user")
    
    def __repr__(self):
        """Return string representation of User instance."""
        return (
            f"<User(user_id={self.user_id}, "
            f"full_name='{self.first_name} {self.last_name}', email='{self.email}')>"
        )
    