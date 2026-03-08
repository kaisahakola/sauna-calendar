from pydantic import BaseModel, Field, field_validator, ConfigDict
import re

class BuildingBase(BaseModel):
  name: str = Field(min_length=2, max_length=100)
  address: str = Field(min_length=2, max_length=100)

  @field_validator("address")
  def address_must_have_number(cls, value):
    if not re.search(r"\d", value):
      raise ValueError("Address must include number")
    
    return value

class BuildingCreate(BuildingBase):
  pass

class Building(BuildingBase):
  id: int
  model_config = ConfigDict(from_attributes=True)
