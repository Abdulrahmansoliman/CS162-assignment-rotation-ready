from typing import Optional, List

from app.repositories.implementations.user_repository import UserRepository
from app.repositories.implementations.rotation_city_repository import RotationCityRepository
from app.models.user import User

class UserService:
    def __init__(
            self,
            user_repository: UserRepository = None,
            rotation_city_repository: RotationCityRepository = None
        ):
        self.user_repository = user_repository or UserRepository()
        self.rotation_city_repository = rotation_city_repository or RotationCityRepository()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by user_id"""
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.user_repository.get_user_by_email(email)
    
    def update_user(self, user_id: int, data: dict) -> Optional[User]:
        """Update user information"""
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return None
        
        if "rotation_city_id" in data:
            data["rotation_city_id"] = \
                self.rotation_city_repository.validate_city_id(data["rotation_city_id"])
            
        self.user_repository.update(user_id, **data)
        return user
    
    def get_verified_user_by_id(self, user_id: int) -> Optional[User]:
        """Get verified user by user_id"""
        user = self.user_repository.get_user_by_id(user_id)
        if user and user.is_verified:
            return user
        return None