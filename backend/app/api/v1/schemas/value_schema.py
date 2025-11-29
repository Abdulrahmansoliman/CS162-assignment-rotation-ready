from pydantic import BaseModel


class ValueSchemaResponse(BaseModel):
    value_id: int
    tag_id: int
    boolean_val: bool
    name_val: str
    numerical_value: float

    model_config = {
        "from_attributes": True
    }