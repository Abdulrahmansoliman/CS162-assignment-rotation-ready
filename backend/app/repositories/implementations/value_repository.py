from typing import Optional, List
from app.models.value import Value
from app.repositories.base.value_interface import (
    IValueRepository
)
from app import db


class ValueRepository(IValueRepository):

    def get_all_values(self) -> List[Value]:
        return db.session.execute(
            db.select(Value)
        ).scalars().all()
    
    def get_value_by_id(self, value_id: int) -> Optional[Value]:
        return db.session.get(Value, value_id)
    
    def add_value(self, 
                  tag_id: int,
                  boolean_val: Optional[bool] = None,
                  name_val: Optional[str] = None,
                  numerical_value: Optional[float] = None) -> Optional[Value]:
        
        try:
            new_value = Value(
                tag_id=tag_id,
                boolean_val=boolean_val,
                name_val=name_val,
                numerical_value=numerical_value
            )
            db.session.add(new_value)
            db.session.commit()
            return new_value
        
        except Exception as e:
            db.session.rollback()
            return None
    
    def update_value(self,
                     value_id: int,
                     tag_id: Optional[int] = None,
                     boolean_val: Optional[bool] = None,
                     name_val: Optional[str] = None,
                     numerical_value: Optional[float] = None) -> Optional[Value]:
        
        value = db.session.get(Value, value_id)

        if not value:
            return None

        try:
            if tag_id is not None:
                value.tag_id = tag_id
            if boolean_val is not None:
                value.boolean_val = boolean_val
            if name_val is not None:
                value.name_val = name_val
            if numerical_value is not None:
                value.numerical_value = numerical_value
            
            db.session.commit()
            return value
        
        except Exception as e:
            db.session.rollback()
            return None
            
    def delete_value(self, value_id: int) -> bool:
        value = db.session.get(Value, value_id)
        if not value:
            return False
        
        try:
            db.session.delete(value)
            db.session.commit()
            return True
        
        except Exception as e:
            db.session.rollback()
            return False