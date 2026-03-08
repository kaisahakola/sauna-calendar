from typing import Literal, Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class BuildingRead(BaseModel):
  id: int
  name: str
  address: str

class UserCreate(BaseModel):
  name: str = Field(min_length=2, max_length=100)
  email: EmailStr
  role: Literal["user", "admin"]
  building_id: Optional[int] = None

class UserRead(BaseModel):
  id: int
  building: Optional[BuildingRead] = None
  model_config = ConfigDict(from_attributes=True)
