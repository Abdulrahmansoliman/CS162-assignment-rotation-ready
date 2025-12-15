"""Category repository implementation."""
from typing import List, Optional
from app import db
from app.models.category import Category
from app.repositories.base.category_repository_interface import (
    CategoryRepositoryInterface
)


class CategoryRepository(CategoryRepositoryInterface):
    """Repository for category data access operations.
    
    Handles all database operations related to item categories.
    """

    def get_all_categories(self) -> List[Category]:
        """Retrieve all categories from the database.
        
        Returns:
            List of all Category objects
        """
        return db.session.execute(db.select(Category)).scalars().all()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Retrieve a category by its ID.
        
        Args:
            category_id: The ID of the category to retrieve
            
        Returns:
            Category object if found, None otherwise
        """
        return db.session.execute(
            db.select(Category).filter_by(category_id=category_id)
        ).scalar_one_or_none()

    def get_categories_by_ids(self, category_ids: List[int]) -> List[Category]:
        """Retrieve multiple categories by their IDs.
        
        Args:
            category_ids: List of category IDs to retrieve
            
        Returns:
            List of Category objects found
        """
        return db.session.execute(
            db.select(Category).filter(Category.category_id.in_(category_ids))
        ).scalars().all()

    def category_exists(self, category_id: int) -> bool:
        """Check if a category exists in the database.
        
        Args:
            category_id: The ID of the category to check
            
        Returns:
            True if category exists, False otherwise
        """
        return self.get_category_by_id(category_id) is not None

    def add_category(
        self,
        category_name: str,
        category_pic: str
    ) -> Optional[Category]:
        """Create a new category in the database.
        
        Args:
            category_name: The name of the category
            category_pic: URL or path to the category picture
            
        Returns:
            Created Category object if successful, None if error occurs
        """
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
        """Update an existing category in the database.
        
        Args:
            category_id: The ID of the category to update
            category_name: Optional new name for the category
            category_pic: Optional new URL or path to category picture
            
        Returns:
            Updated Category object if found, None if not found or error occurs
        """
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

