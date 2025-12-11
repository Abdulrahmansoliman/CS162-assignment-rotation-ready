"""
Category Service
Business logic layer for category operations.
"""
from typing import List, Optional
from app.models.category import Category
from app.repositories.implementations.category_repository import CategoryRepository


class CategoryService:
    """Service for category business logic."""

    def __init__(self):
        self.repository = CategoryRepository()

    def get_all_categories(self) -> List[Category]:
        """Get all categories."""
        return self.repository.get_all_categories()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        return self.repository.get_category_by_id(category_id)

    def add_category(self, category_name: str, category_pic: str) -> Optional[Category]:
        """Create a new category."""
        return self.repository.add_category(category_name, category_pic)

    def update_category(
        self,
        category_id: int,
        category_name: Optional[str] = None,
        category_pic: Optional[str] = None
    ) -> Optional[Category]:
        """Update an existing category."""
        return self.repository.update_category(category_id, category_name, category_pic)

    def delete_category(self, category_id: int) -> bool:
        """Delete a category."""
        return self.repository.delete_category(category_id)
