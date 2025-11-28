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
