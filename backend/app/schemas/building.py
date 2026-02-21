from pydantic import BaseModel

class BuildingBase(BaseModel):
  name: str
  address: str

class BuildingCreate(BuildingBase):
  pass

class Building(BuildingBase):
  id: int
  class Config:
    from_attributes = True
