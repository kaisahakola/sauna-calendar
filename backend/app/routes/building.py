from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.schemas.building import BuildingCreate, Building as BuildingSchema
from app.models.building import Building
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/buildings", response_model=List[BuildingSchema])
def get_all_buildings(db: Session = Depends(get_db)):
  db_buildings = db.query(Building).all()
  return db_buildings

@router.get("/buildings/{building_id}", response_model=BuildingSchema)
def getBuilding_with_id(building_id: int, db: Session = Depends(get_db)):
  db_building = db.get(Building, building_id)
  if not db_building:
    raise HTTPException(status_code=404, detail="Bulding not found")
  
  return db_building

@router.post("/buildings", response_model=BuildingSchema)
def create_building(building: BuildingCreate, db: Session = Depends(get_db)):
  db_building = Building(**building.model_dump())
  db.add(db_building)
  db.commit()
  db.refresh(db_building)
  return db_building

@router.put("/buildings/{building_id}", response_model=BuildingSchema)
def update_building(building_id: int, building: BuildingCreate, db: Session = Depends(get_db)):
  db_building = db.get(Building, building_id)
  if not db_building:
    raise HTTPException(status_code=400, detail="Building not found")
  
  db_building.name = building.name
  db_building.address = building.address

  db.commit()
  db.refresh(db_building)
  return db_building

@router.delete("/buildings/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_building(building_id: int, db: Session = Depends(get_db)):
  db_building = db.get(Building, building_id)
  if not db_building:
    raise HTTPException(status_code=404, detail="Building not found")
  
  db.delete(db_building)
  db.commit()
