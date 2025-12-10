"""Category repository implementation."""
from typing import List, Optional
from app import db
from app.models.category import Category
from app.repositories.base.category_repository_interface import (
    CategoryRepositoryInterface
)


class CategoryRepository(CategoryRepositoryInterface):
    """Repository for category operations."""

    def get_all_categories(self) -> List[Category]:
        """Get all categories."""
        return db.session.execute(db.select(Category)).scalars().all()

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

    def add_category(
        self,
        category_name: str,
        category_pic: str
    ) -> Optional[Category]:
        """Create a new category."""
        try:
            new_category = Category(
                category_name=category_name,
                category_pic=category_pic
            )
            db.session.add(new_category)
            db.session.commit()
            db.session.refresh(new_category)
            return new_category
        except Exception:
            db.session.rollback()
            return None

    def update_category(
        self,
        category_id: int,
        category_name: Optional[str] = None,
        category_pic: Optional[str] = None
    ) -> Optional[Category]:
        """Update an existing category."""
        category = self.get_category_by_id(category_id)

        if not category:
            return None

        try:
            if category_name is not None:
                category.category_name = category_name
            if category_pic is not None:
                category.category_pic = category_pic

            db.session.commit()
            db.session.refresh(category)
            return category
        except Exception:
            db.session.rollback()
            return None

    def delete_category(self, category_id: int) -> bool:
        """Delete a category."""
        category = self.get_category_by_id(category_id)

        if not category:
            return False

        try:
            db.session.delete(category)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

