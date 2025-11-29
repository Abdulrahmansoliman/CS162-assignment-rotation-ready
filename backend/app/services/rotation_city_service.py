"""Rotation city service for business logic"""
from typing import Optional, List
from app.models.rotation_city import RotationCity
from app.repositories.implementations.rotation_city_repository import (
    RotationCityRepository
)


class RotationCityService:
    """Service for rotation city operations"""

    def __init__(
        self,
        rotation_city_repository: RotationCityRepository
    ):
        self.rotation_city_repo = (
            rotation_city_repository or RotationCityRepository()
        )

    def get_rotation_city(self, city_id: int) -> Optional[RotationCity]:
        """Get rotation city by city_id"""
        return self.rotation_city_repo.get_rotation_city_by_id(city_id)

    def get_all_rotation_cities(self) -> List[RotationCity]:
        """Get all rotation cities"""
        return self.rotation_city_repo.get_all_rotation_cities()

    def get_rotation_city_by_name(self, name: str) -> Optional[RotationCity]:
        """Get rotation city by name"""
        return self.rotation_city_repo.get_rotation_city_by_name(name)
