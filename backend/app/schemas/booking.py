from typing import Literal
from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime

class BuildingRead(BaseModel):
  id: int
  name: str
  address: str

class SaunaRead(BaseModel):
  id: int
  name: str

class UserRead(BaseModel):
  id: int
  name: str

class BookingCreate(BaseModel):
  start_time: datetime
  end_time: datetime
  status: Literal["pending", "confirmed", "cancelled"]
  building_id: int
  sauna_id: int
  user_id: int

  @field_validator("end_time")
  def end_after_start(cls, v, info):
    if "start_time" in info.data and v <= info.data["start_time"]:
      raise ValueError("end_time must be after start_time")
    return v

class BookingRead(BaseModel):
  id: int
  building: BuildingRead
  sauna: SaunaRead
  user: UserRead
  model_config = ConfigDict(from_attributes=True)
