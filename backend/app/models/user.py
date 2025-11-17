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
    """
    Represents a user in the system.
    Each user belongs to a rotation city and can add/verify items.
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
    verifications = relationship("Verification", back_populates="user")
    verification_codes = relationship("VerificationCode", back_populates="user")
    
    def __repr__(self):
        return (
            f"<User(user_id={self.user_id}, "
            f"full_name='{self.first_name} {self.last_name}', email='{self.email}')>"
        )

    