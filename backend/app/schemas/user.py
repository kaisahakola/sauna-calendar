from typing import Literal, Optional
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
  name: str = Field(min_length=2, max_length=100)
  email: EmailStr
  role: Literal["user", "admin"]
  building_id: Optional[int] = None

class UserCreate(UserBase):
  pass

class User(UserBase):
  id: int
  class Config:
    from_attributes = True
