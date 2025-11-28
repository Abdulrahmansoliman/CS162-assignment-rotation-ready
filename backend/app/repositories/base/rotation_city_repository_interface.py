from abc import ABC, abstractmethod
from typing import Optional, List
from app.models.rotation_city import RotationCity


class IRotationCityRepository(ABC):
    
    @abstractmethod
    def get_rotation_city_by_id(self, city_id: int) -> Optional[RotationCity]:
        pass
    
    @abstractmethod
    def get_all_rotation_cities(self) -> List[RotationCity]:
        pass
    
    @abstractmethod
    def get_rotation_city_by_name(self, name: str) -> Optional[RotationCity]:
        pass

    @abstractmethod
    def check_city_exists(self, city_id: int) -> bool:
        pass

    @abstractmethod
    def validate_city_id(self, city_id) -> int:
        pass