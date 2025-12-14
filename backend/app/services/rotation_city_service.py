"""Rotation city service for business logic"""
from typing import Optional, List
from app.models.rotation_city import RotationCity
from app.repositories.implementations.rotation_city_repository import (
    RotationCityRepository
)


class RotationCityService:
    """Service for rotation city operations.
    
    Handles business logic for managing Minerva rotation cities.
    """

    def __init__(
        self,
        rotation_city_repository: RotationCityRepository = None
    ):
        """Initialize service with optional dependency injection.
        
        Args:
            rotation_city_repository: Optional RotationCityRepository instance for testing/DI
        """
        self.rotation_city_repo = (
            rotation_city_repository or RotationCityRepository()
        )

    def get_rotation_city(self, city_id: int) -> Optional[RotationCity]:
        """Retrieve a rotation city by its ID.
        
        Args:
            city_id: The ID of the rotation city to retrieve
            
        Returns:
            RotationCity object if found, None otherwise
        """
        return self.rotation_city_repo.get_rotation_city_by_id(city_id)

    def get_all_rotation_cities(self) -> List[RotationCity]:
        """Retrieve all rotation cities.
        
        Returns:
            List of all RotationCity objects
        """
        return self.rotation_city_repo.get_all_rotation_cities()

    def get_rotation_city_by_name(self, name: str) -> Optional[RotationCity]:
        """Retrieve a rotation city by its name.
        
        Args:
            name: The name of the rotation city to retrieve
            
        Returns:
            RotationCity object if found, None otherwise
        """
        return self.rotation_city_repo.get_rotation_city_by_name(name)
