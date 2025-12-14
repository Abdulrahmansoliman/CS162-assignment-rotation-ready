"""
Category Service
Business logic layer for category operations.
"""
from typing import List, Optional
from app.models.category import Category
from app.repositories.implementations.category_repository import CategoryRepository


class CategoryService:
    """Service for category business logic.
    
    Handles business logic for managing item categories.
    """

    def __init__(self):
        """Initialize service with CategoryRepository."""
        self.repository = CategoryRepository()

    def get_all_categories(self) -> List[Category]:
        """Retrieve all categories.
        
        Returns:
            List of all Category objects
        """
        return self.repository.get_all_categories()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Retrieve a category by its ID.
        
        Args:
            category_id: The ID of the category to retrieve
            
        Returns:
            Category object if found, None otherwise
        """
        return self.repository.get_category_by_id(category_id)

    def add_category(self, category_name: str, category_pic: str) -> Optional[Category]:
        """Create a new category.
        
        Args:
            category_name: The name of the category
            category_pic: URL or path to the category picture
            
        Returns:
            Created Category object if successful, None otherwise
        """
        return self.repository.add_category(category_name, category_pic)

    def update_category(
        self,
        category_id: int,
        category_name: Optional[str] = None,
        category_pic: Optional[str] = None
    ) -> Optional[Category]:
        """Update an existing category.
        
        Args:
            category_id: The ID of the category to update
            category_name: Optional new name for the category
            category_pic: Optional new URL or path to category picture
            
        Returns:
            Updated Category object if found, None otherwise
        """
        return self.repository.update_category(category_id, category_name, category_pic)

    def delete_category(self, category_id: int) -> bool:
        """Delete a category.
        
        Args:
            category_id: The ID of the category to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        return self.repository.delete_category(category_id)
