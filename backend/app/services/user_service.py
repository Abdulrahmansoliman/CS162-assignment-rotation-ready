"""User service for business logic"""
from typing import Optional, List
from app.models.user import User
from app.repositories.implementations.user_repository import UserRepository


class UserService:
    """Service for user operations"""

    def __init__(self, user_repository: UserRepository = None):
        self.user_repo = user_repository or UserRepository()

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by user_id"""
        return self.user_repo.get_user_by_id(user_id)

    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self.user_repo.get_all_users()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.user_repo.get_user_by_email(email)
