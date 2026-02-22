from pydantic import BaseModel, Field

class BuildingRead(BaseModel):
  id: int
  name: str
  address: str

  class Config:
    from_attributes = True

class SaunaCreate(BaseModel):
  name: str = Field(max_length=20)
  building_id: int

class SaunaRead(BaseModel):
  id: int
  name: str = Field(max_length=20)
  building: BuildingRead
  class Config:
    from_attributes = True
