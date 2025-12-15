from typing import Optional, List

from app.repositories.implementations.user_repository import UserRepository
from app.repositories.implementations.rotation_city_repository import RotationCityRepository
from app.models.user import User

class UserService:
    """Service for user-related operations.
    
    Handles business logic for user management including retrieval,
    updates, and verification status checks.
    """
    
    def __init__(
            self,
            user_repository: UserRepository = None,
            rotation_city_repository: RotationCityRepository = None
        ):
        """Initialize service with optional dependency injection.
        
        Args:
            user_repository: Optional UserRepository instance for testing/DI
            rotation_city_repository: Optional RotationCityRepository for city validation
        """
        self.user_repository = user_repository or UserRepository()
        self.rotation_city_repository = rotation_city_repository or RotationCityRepository()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            User object if found, None otherwise
        """
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address.
        
        Args:
            email: The email address of the user to retrieve
            
        Returns:
            User object if found, None otherwise
        """
        return self.user_repository.get_user_by_email(email)
    
    def update_user(self, user_id: int, data: dict) -> Optional[User]:
        """Update user information.
        
        Args:
            user_id: The ID of the user to update
            data: Dictionary containing fields to update
            
        Returns:
            Updated User object if found, None otherwise
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return None
        
        if "rotation_city_id" in data:
            data["rotation_city_id"] = \
                self.rotation_city_repository.validate_city_id(data["rotation_city_id"])
            
        self.user_repository.update(user_id, **data)
        return user
    
    def get_verified_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a verified user by their ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            User object if found and verified, None otherwise
        """
        user = self.user_repository.get_user_by_id(user_id)
        if user and user.is_verified:
            return user
        return None