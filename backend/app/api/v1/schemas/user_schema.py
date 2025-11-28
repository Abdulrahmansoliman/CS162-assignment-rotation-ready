from pydantic import BaseModel, ConfigDict
from app.api.v1.schemas.rotation_city_schema import RotationCityResponse


class UserResponse(BaseModel):
    """Response schema for user"""
    user_id: int
    username: str
    email: str | None = None
    full_name: str | None = None
    rotation_city: RotationCityResponse | None = None

    model_config = ConfigDict(from_attributes=True)