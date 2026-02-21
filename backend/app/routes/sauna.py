from typing import List
from fastapi import APIRouter, Depends, HTTPException
from schemas.sauna import SaunaCreate, Sauna as SaunaSchema
from models.sauna import Sauna
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.get("/saunas/", response_model=List[SaunaSchema])
def get_all_saunas(db: Session = Depends(get_db)):
  db_saunas = db.query(Sauna).all()
  return db_saunas

@router.get("/saunas/{sauna_id}", response_model=SaunaSchema)
def get_sauna_with_id(sauna_id: int, db: Session = Depends(get_db)):
  db_sauna = db.get(Sauna, sauna_id)
  if not db_sauna:
    return HTTPException(status_code=400, detail="Sauna not found")

  return db_sauna

@router.post("/saunas/", response_model=SaunaSchema)
def create_sauna(sauna: SaunaCreate, db: Session = Depends(get_db)):
  existing_sauna = db.query(Sauna).filter(Sauna.name == sauna.name and Sauna.building_id == sauna.building_id).first()
  if existing_sauna:
    raise HTTPException(status_code=400, detail="Sauna with this name already exists in the same building")
  
  db_sauna = Sauna(**sauna.model_dump())
  db.add(db_sauna)
  db.commit()
  db.refresh(db_sauna)
  return db_sauna

@router.put("/saunas/{sauna_id}", response_model=SaunaSchema)
def update_sauna(sauna_id: int, sauna: SaunaCreate, db: Session = Depends(get_db)):
  db_sauna = db.get(Sauna, sauna_id)
  if not db_sauna:
    return HTTPException(status_code=400, detail="Sauna not found")
  
  db_sauna.name = sauna.name
  db_sauna.building_id = sauna.building_id

  db.commit()
  db.refresh(db_sauna)
  return db_sauna

@router.delete("/saunas/{sauna_id}")
def delete_sauna(sauna_id: int, db: Session = Depends(get_db)):
  db_sauna = db.get(Sauna, sauna_id)
  if not db_sauna:
    return HTTPException(status_code=400, detail="Sauna not found")
  
  db.delete(db_sauna)
  db.commit()
