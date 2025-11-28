from pydantic import BaseModel, ConfigDict


class RotationCityResponse(BaseModel):
    """Response schema for rotation city"""
    city_id: int
    name: str
    time_zone: str
    res_hall_location: str | None = None

    model_config = ConfigDict(from_attributes=True)
