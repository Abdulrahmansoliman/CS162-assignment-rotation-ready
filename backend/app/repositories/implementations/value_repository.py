"""Value repository implementation."""
from typing import Optional, Union
from app import db
from app.models.value import Value
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

    def find_existing_value(
        self,
        tag_id: int,
        value: Union[bool, str, float],
        value_type: str
    ) -> Optional[Value]:
        """Find existing value for a tag."""
        query = db.select(Value).filter_by(tag_id=tag_id)
        
        # Filter by the appropriate value column
        if value_type == 'boolean':
            query = query.filter_by(boolean_val=bool(value))
        elif value_type == 'text':
            query = query.filter_by(name_val=str(value))
        elif value_type == 'numeric':
            query = query.filter_by(numerical_value=float(value))
        
        return db.session.execute(query).scalar_one_or_none()
