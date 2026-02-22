from pydantic import BaseModel, Field

class SaunaBase(BaseModel):
  name: str = Field(min_length=2, max_length=100)
  building_id: int

class SaunaCreate(SaunaBase):
  pass

class Sauna(SaunaBase):
  id: int
  class Config:
    from_attributes = True
