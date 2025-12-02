"""Value repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, Union
from app.models.value import Value


class ValueRepositoryInterface(ABC):
    """Interface for value repository operations."""

    @abstractmethod
    def create_value(
        self,
        tag_id: int,
        value: Union[bool, str, float],
        value_type: str
    ) -> Value:
        """Create a new value for a tag."""
        pass

    @abstractmethod
    def get_value_by_id(self, value_id: int) -> Optional[Value]:
        """Get value by ID."""
        pass

    @abstractmethod
    def find_existing_value(
        self,
        tag_id: int,
        value: Union[bool, str, float],
        value_type: str
    ) -> Optional[Value]:
        """Find existing value for a tag."""
        pass
