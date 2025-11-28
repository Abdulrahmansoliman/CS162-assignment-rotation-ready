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
    
    def add_category(self, category_name: str, category_pic: Optional[str] = None) -> Category | None:
        try:
            category = Category(
                category_name=category_name,
                category_pic=category_pic
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
        
    def update_category(self, category_id: int, category_name: Optional[str] = None, category_pic: Optional[str] = None) -> Category | None:
        category = db.session.get(Category, category_id)

        if not category:
            return None
        
        try:
            if category_name is not None:
                category.category_name = category_name

            if category_pic is not None:
                category.category_pic = category_pic

            db.session.commit()
            
            return category
        
        except Exception as e:
            db.session.rollback()
            return None
