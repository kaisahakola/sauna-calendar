from fastapi import FastAPI
from app.routes import user, building, sauna, booking

app = FastAPI()

app.include_router(user.router)
app.include_router(building.router)
app.include_router(sauna.router)
app.include_router(booking.router)
