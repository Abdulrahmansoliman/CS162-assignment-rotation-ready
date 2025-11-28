from pydantic import BaseModel, ConfigDict


class CategoryResponse(BaseModel):
    """Response schema for category"""
    category_id: int
    category_name: str
    category_pic: str | None = None

    model_config = ConfigDict(from_attributes=True)