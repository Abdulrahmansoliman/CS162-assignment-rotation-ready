"""Tag API schemas for requests and responses."""
from pydantic import BaseModel, ConfigDict


class TagResponse(BaseModel):
    """Response schema for tag"""
    tag_id: int
    name: str
    value_type: str  # 'boolean', 'text', 'numeric'

    model_config = ConfigDict(from_attributes=True)
