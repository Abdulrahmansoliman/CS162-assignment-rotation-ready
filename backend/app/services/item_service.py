"""Item service for business logic."""
from typing import Union
from app.models.item import Item
from app.models.tag import TagValueType
from app.repositories.implementations.item_repository import ItemRepository
from app.repositories.implementations.category_repository import CategoryRepository
from app.repositories.implementations.category_item_repository import CategoryItemRepository
from app.repositories.implementations.tag_repository import TagRepository
from app.repositories.implementations.value_repository import ValueRepository
from app.repositories.implementations.item_tag_value_repository import ItemTagValueRepository


class ItemService:
    """Service for item-related operations.
    
    Handles business logic for creating, retrieving, and managing items
    along with their associated categories, tags, and values.
    """

    def __init__(
        self,
        item_repository: ItemRepository = None,
        category_repository: CategoryRepository = None,
        category_item_repository: CategoryItemRepository = None,
        tag_repository: TagRepository = None,
        value_repository: ValueRepository = None,
        item_tag_value_repository: ItemTagValueRepository = None
    ):
        """Initialize service with optional dependency injection.
        
        Args:
            item_repository: Optional ItemRepository instance for testing/DI
            category_repository: Optional CategoryRepository for testing/DI
            category_item_repository: Optional CategoryItemRepository for testing/DI
            tag_repository: Optional TagRepository for testing/DI
            value_repository: Optional ValueRepository for testing/DI
            item_tag_value_repository: Optional ItemTagValueRepository for testing/DI
        """
        self.item_repo = item_repository or ItemRepository()
        self.category_repo = category_repository or CategoryRepository()
        self.category_item_repo = category_item_repository or CategoryItemRepository()
        self.tag_repo = tag_repository or TagRepository()
        self.value_repo = value_repository or ValueRepository()
        self.item_tag_value_repo = item_tag_value_repository or ItemTagValueRepository()

    def create_item(
        self,
        name: str,
        location: str,
        rotation_city_id: int,
        added_by_user_id: int,
        category_ids: list[int],
        existing_tags: list[dict],
        new_tags: list[dict],
        walking_distance: float = None
    ) -> Item:
        """
        Create a new item with categories and tags.
        
        Args:
            name: Item name
            location: Item location
            rotation_city_id: City where item is located
            added_by_user_id: User creating the item
            category_ids: List of category IDs
            existing_tags: List of dicts with tag_id and value
            new_tags: List of dicts with name, value_type, and value
            walking_distance: Optional walking distance
            
        Returns:
            Created Item object
            
        Raises:
            ValueError: If validation fails
        """
        # Validate categories exist
        self._validate_categories(category_ids)
        
        # Validate and process tags
        self._validate_tags(existing_tags, new_tags)
        
        # Create the item
        item = self.item_repo.create_item(
            name=name,
            location=location,
            rotation_city_id=rotation_city_id,
            added_by_user_id=added_by_user_id,
            walking_distance=walking_distance
        )
        
        # Link categories to item
        self.category_item_repo.add_categories_to_item(item.item_id, category_ids)
        
        # Process tags
        value_ids = []
        
        # Handle existing tags
        for existing_tag in existing_tags:
            tag_id = existing_tag['tag_id']
            value = existing_tag['value']
            
            # Get tag to know its value_type
            tag = self.tag_repo.get_tag_by_id(tag_id)
            if not tag:
                raise ValueError(f"Tag with ID {tag_id} not found")
            
            # Validate value matches tag's value_type
            self._validate_value_type(value, tag.value_type)
            
            # Get the value_type label for repository methods (they expect strings)
            value_type_label = tag.value_type_label
            value_obj = self.value_repo.create_value(tag_id, value, value_type_label)
            
            value_ids.append(value_obj.value_id)
        
        # Handle new tags
        for new_tag in new_tags:
            tag_name = new_tag['name']
            value_type = new_tag['value_type']
            value = new_tag['value']
            
            # Validate value matches specified value_type
            self._validate_value_type(value, value_type)
            
            # Check if tag name already exists
            existing_tag = self.tag_repo.get_tag_by_name(tag_name)
            if existing_tag:
                raise ValueError(
                    f"Tag '{tag_name}' already exists. "
                    f"Use existing_tags with tag_id {existing_tag.tag_id} instead."
                )
            
            # Create new tag
            tag = self.tag_repo.create_tag(tag_name, value_type)
            
            # Create value for the new tag
            value_obj = self.value_repo.create_value(tag.tag_id, value, value_type)
            value_ids.append(value_obj.value_id)
        
        # Link tag values to item
        if value_ids:
            self.item_tag_value_repo.add_tag_values_to_item(item.item_id, value_ids)
        
        # Reload item with all relationships for response
        return self.get_item_by_id_with_details(item.item_id, rotation_city_id)

    def _validate_categories(self, category_ids: list[int]) -> None:
        """Validate all category IDs exist."""
        categories = self.category_repo.get_categories_by_ids(category_ids)
        found_ids = {cat.category_id for cat in categories}
        missing_ids = set(category_ids) - found_ids
        
        if missing_ids:
            raise ValueError(f"Categories not found: {sorted(missing_ids)}")

    def _validate_tags(self, existing_tags: list[dict], new_tags: list[dict]) -> None:
        """Validate tag data structure and uniqueness."""
        # Validate existing tags reference valid tag IDs
        for existing_tag in existing_tags:
            tag_id = existing_tag.get('tag_id')
            if not tag_id:
                raise ValueError("existing_tags must include tag_id")
            
            tag = self.tag_repo.get_tag_by_id(tag_id)
            if not tag:
                raise ValueError(f"Tag with ID {tag_id} not found")
        
        # Check for duplicate tag names in new_tags
        new_tag_names = [tag['name'].lower() for tag in new_tags]
        if len(new_tag_names) != len(set(new_tag_names)):
            raise ValueError("Duplicate tag names in new_tags are not allowed")

    def _validate_value_type(self, value: Union[bool, str, float], value_type: Union[int, str]) -> None:
        """Validate that value matches the expected value_type.
        
        Args:
            value: The value to validate
            value_type: Either integer code (0, 1, 2) or string label ('boolean', 'text', 'numeric')
        """
        # Convert integer code to string label if needed
        if isinstance(value_type, int):
            try:
                value_type = TagValueType.from_code(value_type).label
            except ValueError:
                raise ValueError(f"Invalid value_type code: {value_type}")
        
        if value_type == 'boolean':
            if not isinstance(value, bool):
                raise ValueError(f"Value must be boolean for value_type 'boolean', got {type(value).__name__}")
        elif value_type == 'text':
            if not isinstance(value, str):
                raise ValueError(f"Value must be string for value_type 'text', got {type(value).__name__}")
        elif value_type == 'numeric':
            if not isinstance(value, (int, float)):
                raise ValueError(f"Value must be numeric for value_type 'numeric', got {type(value).__name__}")

    def get_all_items(self, rotation_city_id: int) -> list[Item]:
        """
        Get all items from specific rotation city.
        
        Args:
            rotation_city_id: ID of the rotation city to filter by
            
        Returns:
            List of all Item objects from the rotation city
        """
        return self.item_repo.get_all_items(rotation_city_id)

    def get_item_by_id(self, item_id: int, rotation_city_id: int) -> Item:
        """
        Get item by ID (must belong to the specified rotation city).
        
        Args:
            item_id: ID of the item to retrieve
            rotation_city_id: ID of the rotation city to filter by
            
        Returns:
            Item object
            
        Raises:
            ValueError: If item not found or doesn't belong to the rotation city
        """
        item = self.item_repo.get_item_by_id(item_id, rotation_city_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found in your rotation city")
        return item

    def _transform_item_for_response(self, item: Item) -> Item:
        """
        Transform item by adding computed properties for API response.
        
        Args:
            item: Item object with relationships loaded
            
        Returns:
            Same item object with categories and tags properties added
        """
        # Transform category_items to categories list
        item.categories = [ci.category for ci in item.category_items]
        
        # Transform item_tag_values to tags list with tag info + values
        tags = []
        for itv in item.item_tag_values:
            if itv.value and itv.value.tag:
                tag_dict = {
                    'tag_id': itv.value.tag.tag_id,
                    'name': itv.value.tag.name,
                    'value_type': itv.value.tag.value_type_label,
                }
                
                # Get the actual value based on value_type (using correct field names)
                value_type_label = itv.value.tag.value_type_label
                if value_type_label == 'boolean':
                    tag_dict['value'] = itv.value.boolean_val
                elif value_type_label == 'text':
                    tag_dict['value'] = itv.value.name_val
                elif value_type_label == 'numeric':
                    tag_dict['value'] = itv.value.numerical_value
                
                tags.append(tag_dict)
        
        item.tags = tags
        return item

    def get_all_items_with_details(self, rotation_city_id: int) -> list[Item]:
        """
        Get all items from rotation city with full relationship data.
        
        Args:
            rotation_city_id: ID of the rotation city to filter by
        
        Returns:
            List of Item objects with relationships loaded and transformed
        """
        items = self.item_repo.get_all_items_with_details(rotation_city_id)
        return [self._transform_item_for_response(item) for item in items]

    def get_item_by_id_with_details(self, item_id: int, rotation_city_id: int) -> Item:
        """
        Get item by ID with full relationship data (must belong to rotation city).
        
        Args:
            item_id: ID of the item to retrieve
            rotation_city_id: ID of the rotation city to filter by
            
        Returns:
            Item object with relationships loaded and transformed
            
        Raises:
            ValueError: If item not found or doesn't belong to the rotation city
        """
        item = self.item_repo.get_item_by_id_with_details(item_id, rotation_city_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found in your rotation city")
        return self._transform_item_for_response(item)

    def get_user_items(self, user_id: int) -> list[Item]:
        """
        Get all items added by a specific user.
        
        Args:
            user_id: ID of the user who added the items
            
        Returns:
            List of Item objects with relationships loaded and transformed
        """
        items = self.item_repo.get_items_by_user(user_id)
        return [self._transform_item_for_response(item) for item in items]
        """
        Get all items.
        
        Returns:
            List of all Item objects
        """
        return self.item_repo.get_all_items()

    def get_item_by_id(self, item_id: int) -> Item:
        """
        Get item by ID.
        
        Args:
            item_id: ID of the item to retrieve
            
        Returns:
            Item object
            
        Raises:
            ValueError: If item not found
        """
        item = self.item_repo.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found")
        return item
