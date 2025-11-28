from typing import Optional, List
from app.models.rotation_city import RotationCity
from app.repositories.base.rotation_city_repository_interface import (
    IRotationCityRepository
)
from app import db


class RotationCityRepository(IRotationCityRepository):
    
    def get_rotation_city_by_id(
        self,
        city_id: int
    ) -> Optional[RotationCity]:
        return db.session.get(RotationCity, city_id)
    
    def get_all_rotation_cities(self) -> List[RotationCity]:
        return db.session.execute(
            db.select(RotationCity)
        ).scalars().all()
    
    def get_rotation_city_by_name(
        self,
        name: str
    ) -> Optional[RotationCity]:
        return db.session.execute(
            db.select(RotationCity).filter_by(name=name)
        ).scalar_one_or_none()
    
    def check_city_exists(self, name: str) -> bool:
        city = db.session.execute(
            db.select(RotationCity).filter_by(name=name)
        ).scalar_one_or_none()
        return city is not None

    def validate_city_id(self, city_id) -> int:
        """Validate and return rotation_city_id"""
        if city_id is None:
            raise ValueError("rotation_city_id cannot be None")
        try:
            city_id = int(city_id)
        except (TypeError, ValueError):
            raise ValueError("rotation_city_id must be an integer")
        if not self.check_city_exists(city_id):
            raise ValueError(f"rotation_city_id {city_id} does not exist")
        return city_id