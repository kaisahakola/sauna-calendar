from pydantic import BaseModel, Field

class BuildingBase(BaseModel):
  name: str = Field(min_length=2, max_length=100)
  address: str = Field(min_length=2, max_length=100)

class BuildingCreate(BuildingBase):
  pass

class Building(BuildingBase):
  id: int
  class Config:
    from_attributes = True
