
from typing import Optional
from app.models.value import Value
from app.repositories.implementations.value_repository import (
    ValueRepository
)


class ValueService:
    """Service for value operations"""

    def __init__(
            self,
            value_repository: Optional[ValueRepository] = None
            ):
        
        self.value_repo = (
            value_repository or ValueRepository()
        )

    def get_all_values(self):
        """Get all values"""
        return self.value_repo.get_all_values()
    
    def get_value_by_id(self, value_id: int):
        """Get value by id"""
        return self.value_repo.get_value_by_id(value_id)
    
    def add_value(
            self,
            tag_id: int,
            boolean_val: Optional[bool] = None,
            name_val: Optional[str] = None,
            numerical_value: Optional[float] = None,
    ) -> Optional[Value]:
        """Add a new value"""

        return self.value_repo.add_value(
            tag_id=tag_id,
            boolean_val=boolean_val,
            name_val=name_val,
            numerical_value=numerical_value
        )
    
    def update_value(
            self,
            value_id: int,
            numerical_value: Optional[float] = None,
            boolean_val: Optional[bool] = None,
            name_val: Optional[str] = None,
            tag_id: Optional[int] = None

    ) -> Optional[Value]:
        """Update an existing value"""
        return self.value_repo.update_value(
            value_id=value_id,
            boolean_val=boolean_val,
            name_val=name_val,
            numerical_value=numerical_value
        )
    
    def delete_value(self, value_id: int) -> bool:
        """Delete a value by id"""
        return self.value_repo.delete_value(value_id)