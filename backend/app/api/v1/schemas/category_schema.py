"""Category response schema."""
from pydantic import BaseModel


class CategorySchemaResponse(BaseModel):
    """Schema for category response."""
    category_id: int
    category_name: str
    category_pic: str

    model_config = {
        "from_attributes": True
    }
