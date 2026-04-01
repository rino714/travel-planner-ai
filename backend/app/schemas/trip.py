from datetime import date, datetime

from pydantic import BaseModel, Field


class TripCreate(BaseModel):
    spot_ids: list[int] = Field(..., min_length=1)
    start_date: date
    days: int = Field(..., ge=1, le=14)


class ScheduleItem(BaseModel):
    time: str
    type: str  # "spot" | "move" | "accommodation"
    name: str
    duration_min: int | None = None
    from_spot: str | None = Field(None, alias="from")
    to_spot: str | None = Field(None, alias="to")

    model_config = {"populate_by_name": True}


class DaySchedule(BaseModel):
    day: int
    date: str
    items: list[ScheduleItem]


class TripResponse(BaseModel):
    id: int
    start_date: date
    days: int
    schedule: list[DaySchedule]
    created_at: datetime

    model_config = {"from_attributes": True}
