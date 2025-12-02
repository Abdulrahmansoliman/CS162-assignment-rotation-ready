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

    @abstractmethod
    def add_value(self, 
                  tag_id: int,
                  boolean_val: Optional[bool] = None,
                  name_val: Optional[str] = None,
                  numerical_value: Optional[float] = None) -> Optional[Value]:
        pass

    @abstractmethod
    def update_value(self,
                     value_id: int,
                     tag_id: Optional[int] = None,
                     boolean_val: Optional[bool] = None,
                     name_val: Optional[str] = None,
                     numerical_value: Optional[float] = None) -> Optional[Value]:
        pass

    @abstractmethod
    def delete_value(self, value_id: int) -> bool:
        pass