from typing import Literal
from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime

class BuildingRead(BaseModel):
  id: int
  name: str
  address: str
  duration_minutes: int

class SaunaRead(BaseModel):
  id: int
  name: str

class UserRead(BaseModel):
  id: int
  name: str

class BookingCreate(BaseModel):
  start_time: datetime
  building_id: int
  sauna_id: int
  user_id: int

class BookingRead(BaseModel):
  id: int
  start_time: datetime
  end_time: datetime
  status: Literal["pending", "confirmed", "cancelled"]
  building: BuildingRead
  sauna: SaunaRead
  user: UserRead
  model_config = ConfigDict(from_attributes=True)
