"""Item repository implementation."""
from typing import Optional
from sqlalchemy.orm import joinedload
from app import db
from app.models.item import Item
from app.models.category_item import CategoryItem
from app.models.item_tag_value import ItemTagValue
from app.models.value import Value
from app.repositories.base.item_repository_interface import ItemRepositoryInterface


class ItemRepository(ItemRepositoryInterface):
    """Repository for item data access operations.
    
    Handles all database operations related to items shared by students.
    """

    def create_item(
        self,
        name: str,
        location: str,
        rotation_city_id: int,
        added_by_user_id: int,
        walking_distance: Optional[float] = None
    ) -> Item:
        """Create a new item in the database.
        
        Args:
            name: The name/title of the item
            location: Physical location of the item
            rotation_city_id: ID of the city where item is located
            added_by_user_id: ID of the user adding the item
            walking_distance: Optional walking distance in appropriate units
            
        Returns:
            Created Item object
        """
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

    def get_item_by_id(self, item_id: int, rotation_city_id: int) -> Optional[Item]:
        """Retrieve an item by ID if it belongs to the specified city.
        
        Args:
            item_id: The ID of the item to retrieve
            rotation_city_id: The rotation city ID to filter by
            
        Returns:
            Item object if found in the specified city, None otherwise
        """
        return db.session.execute(
            db.select(Item).filter_by(item_id=item_id, rotation_city_id=rotation_city_id)
        ).scalar_one_or_none()

    def get_all_items(self, rotation_city_id: int) -> list[Item]:
        """Retrieve all items from a specific rotation city.
        
        Args:
            rotation_city_id: The rotation city ID to filter by
            
        Returns:
            List of Item objects ordered by creation date (newest first)
        """
        return db.session.execute(
            db.select(Item)
            .filter_by(rotation_city_id=rotation_city_id)
            .order_by(Item.created_at.desc())
        ).scalars().all()

    def get_all_items_with_details(self, rotation_city_id: int) -> list[Item]:
        """Retrieve all items with relationships eagerly loaded.
        
        Preloads rotation_city, added_by_user, categories, tags and values
        to avoid N+1 query problems.
        
        Args:
            rotation_city_id: The rotation city ID to filter by
            
        Returns:
            List of Item objects with all relationships loaded
        """
        result = db.session.execute(
            db.select(Item)
            .filter_by(rotation_city_id=rotation_city_id)
            .order_by(Item.created_at.desc())
            .options(
                joinedload(Item.rotation_city),
                joinedload(Item.added_by_user),
                joinedload(Item.category_items).joinedload(CategoryItem.category),
                joinedload(Item.item_tag_values).joinedload(ItemTagValue.value).joinedload(Value.tag)
            )
        )
        return result.scalars().unique().all()

    def get_item_by_id_with_details(self, item_id: int, rotation_city_id: int) -> Optional[Item]:
        """Retrieve an item by ID with all relationships eagerly loaded.
        
        Preloads rotation_city, added_by_user, categories, tags and values.
        Only returns item if it belongs to the specified rotation city.
        
        Args:
            item_id: The ID of the item to retrieve
            rotation_city_id: The rotation city ID to filter by
            
        Returns:
            Item object with all relationships loaded if found, None otherwise
        """
        result = db.session.execute(
            db.select(Item)
            .filter_by(item_id=item_id, rotation_city_id=rotation_city_id)
            .options(
                joinedload(Item.rotation_city),
                joinedload(Item.added_by_user),
                joinedload(Item.category_items).joinedload(CategoryItem.category),
                joinedload(Item.item_tag_values).joinedload(ItemTagValue.value).joinedload(Value.tag)
            )
        )
        return result.unique().scalar_one_or_none()
