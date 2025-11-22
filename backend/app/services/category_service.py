from app.models.category import Category


class CategoryService:
    @staticmethod
    def get_all_categories():
        """Retrieve all categories"""
        return Category.query.all()
    
    @staticmethod
    def get_category(category_id: int):
        """Retrieve a category by ID"""
        return Category.query.filter_by(category_id=category_id).first()
