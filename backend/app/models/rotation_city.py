"""
RotationCity Model
Represents a rotation city where users are assigned during their
Minerva rotation. Contains city information and residential hall location.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app import db


class RotationCity(db.Model):
    """Represents a Minerva rotation city where users are assigned.
    
    Contains city information and residential hall location.
    Examples: San Francisco, Berlin, Buenos Aires, Seoul, etc.
    
    Attributes:
        city_id (int): Primary key, auto-incrementing
        name (str): Unique city name (max 100 chars)
        time_zone (str): City timezone identifier (max 50 chars)
        res_hall_location (str): Residential hall address/location (max 200 chars)
        users: Relationship to users assigned to this city
        items: Relationship to items located in this city
    """
    __tablename__ = 'rotation_city'
    
    # Primary Key with descriptive name
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # City Information
    name = Column(String(100), nullable=False, unique=True)
    time_zone = Column(String(50), nullable=False)
    res_hall_location = Column(String(200), nullable=True)
    
    # Relationships
    users = relationship(
        "User",
        back_populates="rotation_city",
        cascade="all, delete-orphan"
    )
    items = relationship(
        "Item",
        back_populates="rotation_city",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        """Return string representation of RotationCity instance."""
        return (
            f"<RotationCity(city_id={self.city_id}, "
            f"name='{self.name}', time_zone='{self.time_zone}')>"
        )
