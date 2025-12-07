"""Category-Item junction repository."""
from app import db
from app.models.category_item import CategoryItem


class CategoryItemRepository:
    """Repository for category-item junction table operations."""

    def add_category_to_item(self, item_id: int, category_id: int) -> CategoryItem:
        """Link a category to an item."""
        category_item = CategoryItem(
            item_id=item_id,
            category_id=category_id
        )
        db.session.add(category_item)
        return category_item

    def add_categories_to_item(self, item_id: int, category_ids: list[int]) -> None:
        """Link multiple categories to an item."""
        for category_id in category_ids:
            self.add_category_to_item(item_id, category_id)
        db.session.commit()
