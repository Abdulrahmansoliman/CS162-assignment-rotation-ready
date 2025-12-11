"""Value API schemas for requests and responses."""
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ValueSchemaResponse(BaseModel):
    """Response schema for value."""
    value_id: int
    tag_id: int
    boolean_val: Optional[bool] = None
    name_val: Optional[str] = None
    numerical_value: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
