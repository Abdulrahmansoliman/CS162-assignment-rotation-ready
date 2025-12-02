"""Category repository implementation."""
from typing import List, Optional
from app import db
from app.models.category import Category
from app.repositories.base.category_repository_interface import CategoryRepositoryInterface


class CategoryRepository(CategoryRepositoryInterface):
    """Repository for category operations."""

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        return db.session.execute(
            db.select(Category).filter_by(category_id=category_id)
        ).scalar_one_or_none()

    def get_categories_by_ids(self, category_ids: List[int]) -> List[Category]:
        """Get multiple categories by IDs."""
        return db.session.execute(
            db.select(Category).filter(Category.category_id.in_(category_ids))
        ).scalars().all()

    def category_exists(self, category_id: int) -> bool:
        """Check if category exists."""
        return self.get_category_by_id(category_id) is not None
