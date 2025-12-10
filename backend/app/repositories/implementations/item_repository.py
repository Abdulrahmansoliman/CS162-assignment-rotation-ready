"""Item repository implementation."""
from typing import Optional
from app import db
from app.models.item import Item
from app.repositories.base.item_repository_interface import ItemRepositoryInterface


class ItemRepository(ItemRepositoryInterface):
    """Repository for item operations."""

    def create_item(
        self,
        name: str,
        location: str,
        rotation_city_id: int,
        added_by_user_id: int,
        walking_distance: Optional[float] = None
    ) -> Item:
        """Create a new item."""
        item = Item(
            name=name,
            location=location,
            rotation_city_id=rotation_city_id,
            added_by_user_id=added_by_user_id,
            walking_distance=walking_distance
        )
        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)
        return item

    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        """Get item by ID."""
        return db.session.execute(
            db.select(Item).filter_by(item_id=item_id)
        ).scalar_one_or_none()

    def get_all_items(self) -> list[Item]:
        """Get all items."""
        return db.session.execute(
            db.select(Item)
        ).scalars().all()
