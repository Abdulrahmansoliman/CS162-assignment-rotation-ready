"""Category repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.category import Category


class CategoryRepositoryInterface(ABC):
    """Interface for category repository operations."""

    @abstractmethod
    def get_all_categories(self) -> List[Category]:
        """Get all categories."""
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        pass

    @abstractmethod
    def get_categories_by_ids(self, category_ids: List[int]) -> List[Category]:
        """Get multiple categories by IDs."""
        pass

    @abstractmethod
    def category_exists(self, category_id: int) -> bool:
        """Check if category exists."""
        pass

    @abstractmethod
    def add_category(
        self,
        category_name: str,
        category_pic: str
    ) -> Optional[Category]:
        """Create a new category."""
        pass

    @abstractmethod
    def update_category(
        self,
        category_id: int,
        category_name: Optional[str] = None,
        category_pic: Optional[str] = None
    ) -> Optional[Category]:
        """Update an existing category."""
        pass

    @abstractmethod
    def delete_category(self, category_id: int) -> bool:
        """Delete a category."""
        pass
