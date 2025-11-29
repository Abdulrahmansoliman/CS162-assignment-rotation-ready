from typing import Optional, List
from app.models.value import Value
from app.repositories.base.value_interface import (
    IValueRepository
)
from app import db


class RotationCityRepository(IValueRepository):

    def get_all_values(self) -> List[Value]:
        return db.session.execute(
            db.select(Value)
        ).scalars().all()
    
    def get_value_by_id(self, value_id: int) -> Optional[Value]:
        return db.session.get(Value, value_id)