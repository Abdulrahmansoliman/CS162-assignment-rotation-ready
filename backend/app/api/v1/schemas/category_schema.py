"""Category response schema."""
from pydantic import BaseModel
from typing import Optional


class CategorySchemaResponse(BaseModel):
    """Schema for category response."""
    category_id: int
    category_name: str
    category_pic: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
