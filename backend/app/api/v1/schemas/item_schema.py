from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class CategoryResponse(BaseModel):
    """Response schema for category"""
    category_id: int
    name: str
    pic: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class TagValueResponse(BaseModel):
    """Response schema for tag value"""
    tag_name: str
    value: Optional[str] = None
    boolean_value: Optional[bool] = None
    
    model_config = ConfigDict(from_attributes=True)

class ItemResponse(BaseModel):
    """Response schema for item"""
    item_id: int
    name: str
    location: str
    walking_distance: Optional[float] = None
    number_of_verifications: int
    last_verified_date: Optional[datetime] = None
    categories: List[CategoryResponse] = []
    tags: List[TagValueResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

