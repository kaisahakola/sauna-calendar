from pydantic import BaseModel

class SaunaBase(BaseModel):
  name: str
  building_id: int

class SaunaCreate(SaunaBase):
  pass

class Sauna(SaunaBase):
  id: int
  class Config:
    from_attributes = True
