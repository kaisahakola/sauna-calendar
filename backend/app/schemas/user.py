from typing import Optional
from pydantic import BaseModel
from enum import Enum

class Role(Enum):
  ADMIN = "ADMIN"
  USER = "USER"

class UserBase(BaseModel):
  name: str
  email: str
  role: Role
  building_id: Optional[int] = None

class UserCreate(UserBase):
  pass

class User(UserBase):
  id: int
  class Config:
    from_attributes = True
