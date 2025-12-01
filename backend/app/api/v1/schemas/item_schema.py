"""Item API schemas for requests and responses."""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional, Union


class ExistingTagRequest(BaseModel):
    """Schema for existing tag with value."""
    tag_id: int = Field(..., gt=0, description="ID of existing tag")
    value: Union[bool, str, float] = Field(..., description="Value for the tag")

    model_config = ConfigDict(extra='forbid')


class NewTagRequest(BaseModel):
    """Schema for creating new tag with initial value."""
    name: str = Field(..., min_length=1, max_length=100, description="Tag name")
    value_type: str = Field(..., description="Type: 'text', 'boolean', or 'numeric'")
    value: Union[bool, str, float] = Field(..., description="Initial value for the tag")

    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True
    )

    @field_validator('value_type')
    @classmethod
    def validate_value_type(cls, v: str) -> str:
        """Validate value_type is one of the allowed types."""
        allowed_types = ['text', 'boolean', 'numeric']
        if v not in allowed_types:
            raise ValueError(f"value_type must be one of: {', '.join(allowed_types)}")
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate tag name is not empty after stripping."""
        if not v.strip():
            raise ValueError("Tag name cannot be empty")
        return v.strip()


class CreateItemRequest(BaseModel):
    """Schema for creating a new item."""
    name: str = Field(..., min_length=1, max_length=200, description="Item name")
    location: str = Field(..., min_length=1, max_length=500, description="Item location")
    walking_distance: Optional[float] = Field(None, ge=0, description="Walking distance in meters")
    category_ids: List[int] = Field(..., min_length=1, description="At least one category required")
    existing_tags: List[ExistingTagRequest] = Field(default_factory=list, description="Existing tags with values")
    new_tags: List[NewTagRequest] = Field(default_factory=list, description="New tags to create")

    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True
    )

    @field_validator('name', 'location')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """Validate strings are not empty after stripping."""
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    @field_validator('category_ids')
    @classmethod
    def validate_category_ids(cls, v: List[int]) -> List[int]:
        """Validate category IDs are positive and unique."""
        if not v:
            raise ValueError("At least one category is required")
        
        # Check all are positive
        if any(cat_id <= 0 for cat_id in v):
            raise ValueError("All category IDs must be positive")
        
        # Check for duplicates
        if len(v) != len(set(v)):
            raise ValueError("Duplicate category IDs are not allowed")
        
        return v


class ItemResponse(BaseModel):
    """Response schema for item."""
    item_id: int
    name: str
    location: str
    walking_distance: Optional[float]
    rotation_city_id: int
    added_by_user_id: int
    number_of_verifications: int
    created_at: str

    model_config = ConfigDict(from_attributes=True)
