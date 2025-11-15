"""
User Model
Represents a user in the system. Each user belongs to a rotation city
and can add/verify items.
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

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
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    profile_picture = Column(String(200), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    rotation_city = relationship("RotationCity", back_populates="users")
    added_items = relationship("Item", back_populates="added_by_user")
    verifications = relationship("Verification", back_populates="user")
    
    def __repr__(self):
        return (
            f"<User(user_id={self.user_id}, "
            f"username='{self.username}', email='{self.email}')>"
        )

    