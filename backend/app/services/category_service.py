"""Rotation city service for category logic"""
from typing import Optional, List
from app.models.category import Category
from app.repositories.implementations.category_repository import (
    CategoryRepository
)


class CategoryService:
    """Service for category service"""

    def __init__(
            self,
            category_repository: Optional[CategoryRepository] = None
    ):
        self.category_repo = (
            category_repository or CategoryRepository()
        )

    def get_all_categories(self) -> List[Category]:
        return self.category_repo.get_all_categories()

    def update_category(self, category_id: int, category_name: Optional[str] = None, category_pic: Optional[str] = None) -> Optional[Category]:
        return self.category_repo.update_category(category_id, category_name, category_pic)
    
    def delete_category(self, category_id: int) -> bool:
        return self.category_repo.delete_category(category_id)
    
    def add_category(self, category_name: str, category_pic: str) -> Optional[Category]:
        return self.category_repo.add_category(category_name, category_pic)
    
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.category_repo.get_category_by_id(category_id)