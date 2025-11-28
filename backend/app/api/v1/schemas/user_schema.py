from pydantic import BaseModel, ConfigDict
from app.api.v1.schemas.rotation_city_schema import RotationCityResponse


class UserResponse(BaseModel):
    """Response schema for user"""
    user_id: int
    first_name: str
    last_name: str
    email: str | None = None
    rotation_city: RotationCityResponse | None = None

    model_config = ConfigDict(from_attributes=True)