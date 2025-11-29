from abc import ABC, abstractmethod
from typing import Optional, List
from app.models.value import Value


class IValueRepository(ABC):

    @abstractmethod
    def get_all_values(self) -> List[Value]:
        pass
    
    @abstractmethod
    def get_value_by_id(self, value_id: int) -> Optional[Value]:
        pass 
