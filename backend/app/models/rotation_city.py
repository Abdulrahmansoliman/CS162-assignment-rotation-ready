"""
RotationCity Model
Represents a rotation city where users are assigned during their
Minerva rotation. Contains city information and residential hall location.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class RotationCity(Base):
    """
    Represents a rotation city where users are assigned.
    Contains city information and residential hall location.
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
    
    def __repr__(self):
        return (
            f"<RotationCity(city_id={self.city_id}, "
            f"name='{self.name}', time_zone='{self.time_zone}')>"
        )
