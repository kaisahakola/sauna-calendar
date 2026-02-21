from fastapi import FastAPI
from database import engine
from models.base import Base
import models
from routes import user, building, sauna, booking

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(building.router)
app.include_router(sauna.router)
app.include_router(booking.router)
