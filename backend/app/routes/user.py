from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserLogin, UserRead as UserSchema
from app.models.user import User
from app.models.building import Building
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import password_hash

router = APIRouter()

@router.get("/users", response_model=List[UserSchema])
def get_all_users(db: Session = Depends(get_db)):
  db_users = db.query(User).all()
  return db_users

@router.get("/users/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
  db_user = db.get(User, user_id)
  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")

  return db_user

@router.post("/login", response_model=UserSchema)
def login(user: UserLogin, db: Session = Depends(get_db)):
  db_user = db.query(User).filter(User.email == user.email).first()

  if not db_user:
    raise HTTPException(satus_code=401, detail="Invalid email or password")

  if not password_hash.verify(user.password, db_user.password_hash):
    raise HTTPException(status_code=401, detail="Invalid email or password")

  return db_user

@router.post("/users", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
  existing_user = db.query(User).filter(User.email == user.email).first()
  if existing_user:
    raise HTTPException(status_code=404, detail="Email already registered")

  building = db.get(Building, user.building_id)
  if not building:
    raise HTTPException(status_code=404, detail="Building not found")
  
  db_user = User(
    name=user.name,
    email=user.email,
    password_hash=password_hash.hash(user.password),
    building_id=user.building_id
  )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

@router.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
  db_user = db.get(User, user_id)
  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")

  building = db.get(Building, user.building_id)
  if not building:
    raise HTTPException(status_code=404, detail="Building not found")
  
  db_user.name = user.name
  db_user.email = user.email
  db_user.role = "user"
  db_user.building_id = user.building_id

  db.commit()
  db.refresh(db_user)
  return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
  db_user = db.get(User, user_id)
  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")
  
  db.delete(db_user)
  db.commit()
