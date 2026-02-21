from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
  name: str
  email: str
  role: str
  building_id: Optional[int] = None

class UserCreate(UserBase):
  pass

class User(UserBase):
  id: int
  class Config:
    from_attributes = True
