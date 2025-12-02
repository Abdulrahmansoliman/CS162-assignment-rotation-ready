"""Tag repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.tag import Tag


class TagRepositoryInterface(ABC):
    """Interface for tag repository operations."""

    @abstractmethod
    def get_all_tags(self) -> List[Tag]:
        """Get all tags."""
        pass

    @abstractmethod
    def get_tag_by_id(self, tag_id: int) -> Optional[Tag]:
        """Get tag by ID."""
        pass

    @abstractmethod
    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        """Get tag by name."""
        pass

    @abstractmethod
    def create_tag(self, name: str, value_type: str) -> Tag:
        """Create a new tag."""
        pass
