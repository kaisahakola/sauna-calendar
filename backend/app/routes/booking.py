from typing import List
from fastapi import APIRouter, Depends, HTTPException
from schemas.booking import BookingCreate, Booking as BookingSchema
from models.booking import Booking
from models.building import Building
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

@router.get("/bookings", response_model=List[BookingSchema])
def get_all_bookings(db: Session = Depends(get_db)):
  db_bookings = db.query(Booking).all()
  return db_bookings

@router.get("/bookings/{booking_id}", response_model=BookingSchema)
def get_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
  db_booking = db.get(Booking, booking_id)
  if not db_booking:
    return HTTPException(status_code=400, detail="Booking not found")

  return db_booking

@router.post("/bookings", response_model=BookingSchema)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
  building = db.get(Building, booking.building_id)
  if not building:
    raise HTTPException(status_code=400, detail="Building not found")

  sauna = db.get(Sauna, booking.sauna_id)
  if not sauna:
    raise HTTPException(status_code=400, detail="Sauna not found")
  
  if sauna.building_id != booking.building_id:
    raise HTTPException(status_code=400, detail="Sauna does not exist in the selected building")
  
  overlapping_sauna_booking = db.query(Booking).filter(
    Booking.sauna_id == booking.sauna_id,
    Booking.start_time < booking.end_time,
    Booking.end_time > booking.start_time
  ).first()

  if overlapping_sauna_booking:
    raise HTTPException(status_code=400, detail="Sauna already booked for this time")
  
  overlapping_user_booking = db.query(Booking).filter(
    Booking.user_id == booking.user_id,
    Booking.start_time < booking.end_time,
    Booking.end_time > booking.start_time
  ).first()

  if overlapping_user_booking:
    raise HTTPException(status_code=400, detail="User already booked sauna for this time")
  
  db_booking = Booking(**booking.model_dump())
  db.add(db_booking)
  db.commit()
  db.refresh(db_booking)
  return db_booking

@router.put("/bookings/{booking_id}", response_model=BookingSchema)
def update_booking(booking_id: int, booking: BookingCreate, db: Session = Depends(get_db)):
  db_booking = db.get(Booking, booking_id)
  if not db_booking:
    raise HTTPException(status_code=400, detail="Booking not found")
  
  db_booking.start_time = booking.start_time
  db_booking.end_time = booking.end_time
  db_booking.status = booking.status
  db_booking.building_id = booking.building_id
  db_booking.sauna_id = booking.sauna_id
  db_booking.user_id = booking.user_id

  db.commit()
  db.refresh(db_booking)
  return db_booking

@router.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
  db_booking = db.get(Booking, booking_id)
  if not db_booking:
    raise HTTPException(status_code=400, detail="Booking not found")
  
  db.delete(db_booking)
  db.commit()
