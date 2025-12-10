"""Value service for business logic."""
from typing import List, Optional
from app.models.value import Value
from app.models.tag import Tag
from app.repositories.implementations.value_repository import ValueRepository
from app import db


class ValueService:
    """Service for value-related operations."""

    def __init__(self, value_repository: ValueRepository = None):
        self.value_repository = value_repository or ValueRepository()

    def get_all_values(self) -> List[Value]:
        """Get all values."""
        return db.session.execute(db.select(Value)).scalars().all()

    def get_value_by_id(self, value_id: int) -> Optional[Value]:
        """Get value by ID."""
        return self.value_repository.get_value_by_id(value_id)

    def get_text_values_by_tag(self, tag_id: int) -> List[Value]:
        """Get all text values for a specific tag.
        
        Only returns values where:
        - tag_id matches
        - The tag's value_type is 'text'
        - name_val is not None
        """
        # Query values with their associated tag
        query = (
            db.select(Value)
            .join(Tag, Value.tag_id == Tag.tag_id)
            .filter(Value.tag_id == tag_id)
            .filter(Tag.value_type == 'text')
            .filter(Value.name_val.isnot(None))
        )
        
        return db.session.execute(query).scalars().all()

    def add_value(
        self,
        tag_id: int,
        boolean_val: Optional[bool] = None,
        name_val: Optional[str] = None,
        numerical_value: Optional[float] = None
    ) -> Optional[Value]:
        """Create new value."""
        value = Value(
            tag_id=tag_id,
            boolean_val=boolean_val,
            name_val=name_val,
            numerical_value=numerical_value
        )
        db.session.add(value)
        db.session.commit()
        db.session.refresh(value)
        return value

    def update_value(
        self,
        value_id: int,
        tag_id: Optional[int] = None,
        boolean_val: Optional[bool] = None,
        name_val: Optional[str] = None,
        numerical_value: Optional[float] = None
    ) -> Optional[Value]:
        """Update value."""
        value = self.get_value_by_id(value_id)
        if not value:
            return None

        if tag_id is not None:
            value.tag_id = tag_id
        if boolean_val is not None:
            value.boolean_val = boolean_val
        if name_val is not None:
            value.name_val = name_val
        if numerical_value is not None:
            value.numerical_value = numerical_value

        db.session.commit()
        db.session.refresh(value)
        return value

    def delete_value(self, value_id: int) -> bool:
        """Delete value."""
        value = self.get_value_by_id(value_id)
        if not value:
            return False

        db.session.delete(value)
        db.session.commit()
        return True
