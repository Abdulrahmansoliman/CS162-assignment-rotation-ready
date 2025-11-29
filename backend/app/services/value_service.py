
from typing import Optional, List
from app.models.value import Value
from app.repositories.implementations.value_repository import (
    ValueRepository
)


class ValueService:
    """Service for value operations"""

    def __init__(
            self,
            value_repository: ValueRepository = None
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