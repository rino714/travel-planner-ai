from datetime import datetime

from pydantic import BaseModel, Field


class SpotCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: str | None = None
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class SpotResponse(BaseModel):
    id: int
    name: str
    address: str | None
    lat: float
    lng: float
    created_at: datetime

    model_config = {"from_attributes": True}
