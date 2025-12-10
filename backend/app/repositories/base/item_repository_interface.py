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
    def get_item_by_id(self, item_id: int, rotation_city_id: int) -> Optional[Item]:
        """Get item by ID (filtered by rotation city)."""
        pass

    @abstractmethod
    def get_all_items(self, rotation_city_id: int) -> list[Item]:
        """Get all items (filtered by rotation city)."""
        pass

    @abstractmethod
    def get_all_items_with_details(self, rotation_city_id: int) -> list[Item]:
        """Get all items with relationships loaded (filtered by rotation city)."""
        pass

    @abstractmethod
    def get_item_by_id_with_details(self, item_id: int, rotation_city_id: int) -> Optional[Item]:
        """Get item by ID with relationships loaded (filtered by rotation city)."""
        pass
