from pydantic import BaseModel
from typing import Literal, Optional

class UserBase(BaseModel):
  name: str
  email: str
  role: Literal["user", "admin"]
  building_id: Optional[int] = None

class UserCreate(UserBase):
  pass

class User(UserBase):
  id: int
  class Config:
    from_attributes = True
