"""Category repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.category import Category


class CategoryRepositoryInterface(ABC):
    """Interface for category repository operations."""

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
