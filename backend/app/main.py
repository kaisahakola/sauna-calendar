from fastapi import FastAPI
from database import engine
from models import Base
from models import user, building, sauna, booking

app = FastAPI()
Base.metadata.create_all(bind=engine)
