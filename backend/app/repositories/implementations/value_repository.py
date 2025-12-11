"""Value repository implementation."""
from typing import List, Optional, Union
from app import db
from app.models.value import Value
from app.models.tag import Tag, TagValueType
from app.repositories.base.value_repository_interface import ValueRepositoryInterface


class ValueRepository(ValueRepositoryInterface):
    """Repository for value operations."""

    def create_value(
        self,
        tag_id: int,
        value: Union[bool, str, float],
        value_type: str
    ) -> Value:
        """Create a new value for a tag."""
        value_obj = Value(tag_id=tag_id)
        
        # Set the appropriate column based on value_type
        if value_type == 'boolean':
            value_obj.boolean_val = bool(value)
        elif value_type == 'text':
            value_obj.name_val = str(value)
        elif value_type == 'numeric':
            value_obj.numerical_value = float(value)
        
        db.session.add(value_obj)
        db.session.commit()
        db.session.refresh(value_obj)
        return value_obj

    def get_value_by_id(self, value_id: int) -> Optional[Value]:
        """Get value by ID."""
        return db.session.execute(
            db.select(Value).filter_by(value_id=value_id)
        ).scalar_one_or_none()

    def get_all_values(self) -> List[Value]:
        """Get all values in the system.
        
        Returns:
            List of all Value objects
        """
        return db.session.execute(db.select(Value)).scalars().all()

    def get_text_values_by_tag(self, tag_id: int) -> List[Value]:
        """Get all text values for a specific tag.
        
        Only returns values where:
        - tag_id matches
        - The tag's value_type is TEXT (code=1)
        - name_val is not None
        
        Args:
            tag_id: ID of the tag to filter by
            
        Returns:
            List of text values for the tag
        """
        query = (
            db.select(Value)
            .join(Tag, Value.tag_id == Tag.tag_id)
            .filter(Value.tag_id == tag_id)
            .filter(Tag.value_type == TagValueType.TEXT.code)
            .filter(Value.name_val.isnot(None))
        )
        
        return db.session.execute(query).scalars().all()

    def update_value(
        self,
        value_id: int,
        value_type: Optional[Union[str, int]] = None,
        boolean_val: Optional[bool] = None,
        name_val: Optional[str] = None,
        numerical_value: Optional[float] = None
    ) -> Optional[Value]:
        """Update an existing value.
        
        Args:
            value_id: ID of the value to update
            value_type: New value type (optional)
            boolean_val: New boolean value (optional)
            name_val: New text value (optional)
            numerical_value: New numeric value (optional)
            
        Returns:
            Updated Value object or None if not found
        """
        value = self.get_value_by_id(value_id)
        if not value:
            return None

        if value_type is not None:
            # Convert string labels to integer codes if needed
            if isinstance(value_type, str):
                value_type = TagValueType.from_label(value_type).code
        
            if value_type == TagValueType.BOOLEAN.code:
                value.boolean_val = boolean_val
                value.name_val = None
                value.numerical_value = None
            elif value_type == TagValueType.TEXT.code:
                value.name_val = name_val
                value.boolean_val = None
                value.numerical_value = None
            elif value_type == TagValueType.NUMERIC.code:
                value.numerical_value = numerical_value
                value.boolean_val = None
                value.name_val = None

        db.session.commit()
        db.session.refresh(value)
        return value

    def find_similar_text_values(
        self,
        tag_id: int,
        value: str
    ) -> List[Value]:
        """Find similar text values for a tag."""
        # use like to allow partial matches
        return db.session.execute(
            db.select(Value)
            .join(Tag, Value.tag_id == Tag.tag_id)
            .filter(Value.tag_id == tag_id)
            .filter(Tag.value_type == TagValueType.TEXT.code)
            .filter(Value.name_val.ilike(f"%{value}%"))
        ).scalars().all()