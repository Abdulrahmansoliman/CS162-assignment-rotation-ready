"""Tag API schemas for requests and responses."""
from pydantic import BaseModel, ConfigDict, field_validator


class TagResponse(BaseModel):
    """Response schema for tag"""
    tag_id: int
    name: str
    value_type: str  # 'boolean', 'text', 'numeric'

    model_config = ConfigDict(from_attributes=True)

    @field_validator('value_type', mode='before')
    @classmethod
    def convert_value_type_code_to_label(cls, v):
        """Convert integer value_type code to string label."""
        from app.models.tag import TagValueType
        
        if isinstance(v, int):
            return TagValueType.from_code(v).label
        return v
