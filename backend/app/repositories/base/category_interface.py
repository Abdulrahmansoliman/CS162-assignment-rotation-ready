from abc import ABC, abstractmethod
from typing import Optional, List
from app.models.category import Category


class ICategoryRepository(ABC):

    @abstractmethod
    def get_all_categories(self) -> List[Category]:
        pass

    @abstractmethod
    def add_category(self, category_name: str, category_pic: str) -> Optional[Category]:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def delete_category(self, category_id: int) -> bool:
        pass

    @abstractmethod
    def update_category(self, category_id: int, category_name: str, category_pic: str) -> Optional[Category]:
        pass
