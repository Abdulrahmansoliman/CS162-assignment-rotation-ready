"""Value service for business logic."""
from typing import List, Optional
from app.models.value import Value
from app.models.tag import TagValueType
from app.repositories.implementations.value_repository import ValueRepository
from app.repositories.implementations.tag_repository import TagRepository


class ValueService:
    """Service for value-related operations.
    
    Handles business logic for value management, delegating
    all data access to ValueRepository following the repository pattern.
    This service layer contains NO database interactions.
    """

    def __init__(
            self,
            value_repository: ValueRepository = None,
            tag_repository: TagRepository = None
    )   -> None:
        """Initialize service with optional dependency injection.
        
        Args:
            value_repository: Optional ValueRepository instance for testing/DI
        """
        self.value_repository = value_repository or ValueRepository()
        self.tag_repository = tag_repository or TagRepository()

    def get_value_by_id(self, value_id: int) -> Optional[Value]:
        """Get value by ID.
        
        Args:
            value_id: ID of the value to retrieve
            
        Returns:
            Value object or None if not found
        """
        return self.value_repository.get_value_by_id(value_id)

    def get_all_values(self) -> List[Value]:
        """Get all values in the system.
        
        Returns:
            List of all Value objects
        """
        return self.value_repository.get_all_values()

    def get_text_values_by_tag(self, tag_id: int) -> List[Value]:
        """Get all text values for a specific tag.
        
        Only returns values where:
        - tag_id matches
        - The tag's value_type is TEXT
        - name_val is not None
        
        Args:
            tag_id: ID of the tag to filter by
            
        Returns:
            List of text values for the tag
        """
        return self.value_repository.get_text_values_by_tag(tag_id)

    def add_value(
        self,
        tag_id: int,
        boolean_val: Optional[bool] = None,
        name_val: Optional[str] = None,
        numerical_value: Optional[float] = None
    ) -> Optional[Value]:
        """Create new value.
        
        Note: This method is kept for backward compatibility.
        Internally delegates to repository for data access.
        
        Args:
            tag_id: ID of the tag this value belongs to
            boolean_val: Boolean value (optional)
            name_val: Text value (optional)
            numerical_value: Numeric value (optional)
            
        Returns:
            Created Value object
        """
        # Determine value_type based on tag_id
        tag = self.tag_repository.get_tag_by_id(tag_id)
        if not tag:
            return None

        if tag.value_type == TagValueType.BOOLEAN and boolean_val is not None:
            return self.value_repository.create_value(tag_id, boolean_val, TagValueType.BOOLEAN.value)
        elif tag.value_type == TagValueType.TEXT and name_val is not None:
            return self.value_repository.create_value(tag_id, name_val, TagValueType.TEXT.value)
        elif tag.value_type == TagValueType.NUMERIC and numerical_value is not None:
            return self.value_repository.create_value(tag_id, numerical_value, TagValueType.NUMERIC.value)

        return None

    def update_value(
        self,
        value_id: int,
        boolean_val: Optional[bool] = None,
        name_val: Optional[str] = None,
        numerical_value: Optional[float] = None
    ) -> Optional[Value]:
        """Update an existing value.
        
        Args:
            value_id: ID of the value to update
            boolean_val: New boolean value (optional)
            name_val: New text value (optional)
            numerical_value: New numeric value (optional)
            
        Returns:
            Updated Value object or None if not found
        """
        value = self.value_repository.get_value_by_id(value_id)

        if not value:
            return None

        value_type = self.tag_repository.get_tag_by_id(value.tag_id).value_type

        return self.value_repository.update_value(
            value_id=value_id,
            value_type=value_type,
            boolean_val=boolean_val,
            name_val=name_val,
            numerical_value=numerical_value
        )
    
    def find_similar_text_values(
        self,
        tag_id: int,
        value: str
    ) -> List[Value]:
        """Find similar text values for a tag.

        Args:
            tag_id: ID of the tag to search within
            value: Text value to find similar for

        Returns:
            List of similar Value objects or an empty list if none found
        """
        tag = self.tag_repository.get_tag_by_id(tag_id)
        if not tag or tag.value_type != TagValueType.TEXT:
            return []
        return self.value_repository.find_similar_text_values(tag_id, value)