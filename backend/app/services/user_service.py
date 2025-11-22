"""User service for business logic"""
from typing import Optional
from app.models.user import User


class UserService:
    """Service for user operations"""

    @staticmethod
    def get_user(user_id: int) -> Optional[User]:
        """Get user by user_id"""
        return User.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_all_users() -> list[User]:
        """Get all users"""
        return User.query.all()

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        return User.query.filter_by(email=email).first()
