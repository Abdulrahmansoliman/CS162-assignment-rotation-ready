from pydantic import BaseModel
from typing import Optional


class ValueSchemaResponse(BaseModel):
    value_id: int
    tag_id: int
    boolean_val: Optional[bool] = None
    name_val: Optional[str] = None
    numerical_value: Optional[float] = None

    model_config = {
        "from_attributes": True
    }