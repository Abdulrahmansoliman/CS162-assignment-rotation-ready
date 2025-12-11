"""Value repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional, Union
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
    def get_all_values(self) -> List[Value]:
        """Get all values in the system."""
        pass

    @abstractmethod
    def get_text_values_by_tag(self, tag_id: int) -> List[Value]:
        """Get all text values for a specific tag."""
        pass

    @abstractmethod
    def update_value(
        self,
        value_id: int,
        tag_id: Optional[int] = None,
        boolean_val: Optional[bool] = None,
        name_val: Optional[str] = None,
        numerical_value: Optional[float] = None
    ) -> Optional[Value]:
        """Update an existing value."""
        pass

    @abstractmethod
    def find_similar_text_values(
        self,
        tag_id: int,
        value: str
    ) -> List[Value]:
        """Find a similar text value for a tag."""
        pass
