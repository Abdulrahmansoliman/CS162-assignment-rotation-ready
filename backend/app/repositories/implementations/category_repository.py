from typing import Optional, List
from app.models.category import Category
from app.repositories.base.category_interface import ICategoryRepository
from app import db


class CategoryRepository(ICategoryRepository):

    def get_all_categories(self) -> List[Category]:
        return db.session.execute(
            db.select(Category)
        ).scalars().all()
    
    def get_category_by_id(self, category_id: int) -> Category | None:
        return db.session.execute(
            db.select(Category).filter_by(category_id=category_id)
        ).scalar_one_or_none()
    
    def add_category(self, name: str, pic: str) -> Category | None:
        try:
            category = Category(
                category_name=name,
                category_pic=pic
            )

            db.session.add(category)
            db.session.commit()

            return category
        
        except Exception as e:
            db.session.rollback()
            return None
    
    def delete_category(self, category_id: int) -> bool:
        category = db.session.get(Category, category_id)
        
        if not category:
            return False
        
        try:
            db.session.delete(category)
            db.session.commit()
            return True
        
        except Exception as e:
            db.session.rollback()
            return False
        
    def update_category(self, category_id: int, name: str, pic: str) -> Category | None:
        category = db.session.get(Category, category_id=category_id)

        if not category:
            return None
        
        try:
            if name is not None:
