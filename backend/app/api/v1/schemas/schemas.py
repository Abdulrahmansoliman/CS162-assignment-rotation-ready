from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ItemResponse(BaseModel):
    """Response schema for a single item"""
    item_id: int
    name: str
    location: str
    walking_distance: Optional[float]
    last_verified_date: Optional[datetime]
    added_by_user_id: int 
    created_at: datetime
    number_of_verifications: int
    
    class Config:
        from_attributes = True


class CategoriesResponse(BaseModel):
    """Response schema for categories"""
    category_id: int
    name_name: str
    category_pic: Optional[str] = None

    class Config:
        from_attributes = True


class RotationCityResponse(BaseModel):
    """Response schema for rotation city"""
    city_id: int
    city_name: str
    timezone: str

    class Config:
        from_attributes = True


class ValueResponse(BaseModel):
    """Response schema for value"""
    value_id: int
    tag_id: int
    boolean_val: bool
    name_val: str
    number_val: float

    class Config:
        from_attributes = True