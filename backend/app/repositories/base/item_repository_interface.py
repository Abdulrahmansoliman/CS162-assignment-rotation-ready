"""Item repository interface."""
from abc import ABC, abstractmethod
from typing import Optional
from app.models.item import Item


class ItemRepositoryInterface(ABC):
    """Interface for item repository operations."""

    @abstractmethod
    def create_item(
        self,
        name: str,
        location: str,
        rotation_city_id: int,
        added_by_user_id: int,
        walking_distance: Optional[float] = None
    ) -> Item:
        """Create a new item."""
        pass

    @abstractmethod
    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        """Get item by ID."""
        pass

    @abstractmethod
    def get_all_items(self) -> list[Item]:
        """Get all items."""
        pass
