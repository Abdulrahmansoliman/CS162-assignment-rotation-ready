from abc import ABC, abstractmethod
from typing import Optional
from app.models.verification_code import VerificationCode


class IVerificationCodeRepository(ABC):
    
    @abstractmethod
    def create_registration(self, **kwargs) -> VerificationCode:
        pass
    
    @abstractmethod
    def create_login(self, **kwargs) -> VerificationCode:
        pass
    
    @abstractmethod
    def find_most_recent_active_code(
        self,
        user_id: int,
        code_type: str
    ) -> Optional[VerificationCode]:
        pass
    
    @abstractmethod
    def increase_attempts(self, verification_code_id: int) -> None:
        pass
    
    @abstractmethod
    def mark_as_used(self, verification_code_id: int) -> None:
        pass
    
    @abstractmethod
    def count_recent_codes(
        self,
        user_id: int,
        code_type: str,
        since_minutes: int
    ) -> int:
        pass

    def get_recent_codes_time_window(
        self,
        user_id: int,
        code_type: str,
        since_minutes: int
    ) -> list[VerificationCode]:
        pass