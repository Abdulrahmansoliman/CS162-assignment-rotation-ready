from app.models.item import Item
from app import db


class ItemService:
    @staticmethod
    def create_item(name: str, location: str, added_by_user_id: int, walking_distance: float = None) -> Item:
        """Create and return a new item."""
        new_item = Item(
            name=name,
            location=location,
            added_by_user_id=added_by_user_id,
            walking_distance=walking_distance
        )
        db.session.add(new_item)
        db.session.commit()
        db.session.refresh(new_item)

        return new_item
    
    @staticmethod
    def get_item(item_id: int) -> Item:
        """Retrieve an item by its ID."""
        return Item.query.filter_by(item_id=item_id).first()
    
    @staticmethod
    def get_all_items() -> list[Item]:
        """Retrieve all items."""
        return Item.query.all()