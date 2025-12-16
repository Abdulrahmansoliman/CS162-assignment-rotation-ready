from abc import ABC, abstractmethod
from typing import Optional, List
from app.models.user import User


class IUserRepository(ABC):
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        rotation_city_id: int,
        profile_picture: Optional[str] = None,
    ) -> User:
        pass
    
    @abstractmethod
    def mark_user_as_verified(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass
    
    @abstractmethod
    def update(self, user_id: int, **kwargs) -> User:
        pass
