from datetime import datetime
from pydantic import BaseModel, model_validator, ConfigDict # type: ignore

class SlotBase(BaseModel):
    practitioner_id: int
    start_time: datetime
    end_time: datetime
    is_booked: bool = False

    @model_validator(mode="after")
    def check_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self

class SlotCreate(SlotBase):
    pass

class SlotUpdate(BaseModel):
    practitioner_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    is_booked: bool | None = None

    @model_validator(mode="after")
    def check_times(self):
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self

class SlotRead(SlotBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
