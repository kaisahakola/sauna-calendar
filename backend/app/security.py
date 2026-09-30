import os

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer("/login")
password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict):
  return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  try:
    token_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
  except jwt.DecodeError:
    raise HTTPException(status_code=401, detail="Not authenticated")
  
  user_id = token_payload["sub"]

  db_user = db.get(User, user_id)

  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")

  return db_user
