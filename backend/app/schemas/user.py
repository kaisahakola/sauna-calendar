from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class BuildingRead(BaseModel):
  id: int
  name: str
  address: str

class UserCreate(BaseModel):
  name: str = Field(min_length=2, max_length=100)
  email: EmailStr
  building_id: Optional[int] = None
  password: str = Field(min_length=8)

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class UserRead(BaseModel):
  id: int
  name: str
  email: EmailStr
  role: str
  building: Optional[BuildingRead] = None
  model_config = ConfigDict(from_attributes=True)
