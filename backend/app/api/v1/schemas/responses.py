from pydantic import BaseModel, ConfigDict


class RotationCityResponse(BaseModel):
    """Response schema for rotation city"""
    city_id: int
    name: str
    time_zone: str
    res_hall_location: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CategoryResponse(BaseModel):
    """Response schema for category"""
    category_id: int
    category_name: int
    category_pic: str | None = None

    model_config = ConfigDict(from_attributes=True)
