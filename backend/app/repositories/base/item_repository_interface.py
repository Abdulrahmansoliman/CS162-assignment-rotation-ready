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

    @abstractmethod
    def get_items_by_user(self, user_id: int) -> list[Item]:
        """Get all items added by a specific user with relationships loaded."""
        pass

    @abstractmethod
    def exists(self, item_id: int) -> bool:
        """Check if an item exists by ID.

        Args:
            item_id: The ID of the item to check for existence.

        Returns:
            True if the item exists in the datastore, False otherwise.
        """
        pass

    @abstractmethod
    def update_verification_count(self, item_id: int, count: int) -> None:
        """Update the verification count for an item.

        Args:
            item_id: The ID of the item whose verification count should be updated.
            count: The new verification count to set for the item.

        Returns:
            None

        Raises:
            ValueError: If the specified item does not exist.
        """
        pass