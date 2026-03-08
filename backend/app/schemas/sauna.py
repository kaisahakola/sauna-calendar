from pydantic import BaseModel, Field, ConfigDict

class BuildingRead(BaseModel):
  id: int
  name: str
  address: str
  model_config = ConfigDict(from_attributes=True)

class SaunaCreate(BaseModel):
  name: str = Field(max_length=20)
  building_id: int

class SaunaRead(BaseModel):
  id: int
  name: str = Field(max_length=20)
  building: BuildingRead
  model_config = ConfigDict(from_attributes=True)
