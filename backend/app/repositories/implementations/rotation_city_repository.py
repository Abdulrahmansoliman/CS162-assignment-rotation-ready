from typing import Optional, List
from app.models.rotation_city import RotationCity
from app.repositories.base.rotation_city_repository_interface import (
    IRotationCityRepository
)


class RotationCityRepository(IRotationCityRepository):
    
    def get_rotation_city_by_id(
        self,
        city_id: int
    ) -> Optional[RotationCity]:
        return RotationCity.query.get(city_id)
    
    def get_all_rotation_cities(self) -> List[RotationCity]:
        return RotationCity.query.all()
    
    def get_rotation_city_by_name(
        self,
        name: str
    ) -> Optional[RotationCity]:
        return RotationCity.query.filter_by(name=name).first()
