from models import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Booking(Base):
  __tablename__ = "bookings"
  id = Column(Integer, primary_key=True)
  start_time = Column(DateTime)
  end_time = Column(DateTime)
  status = Column(String)
  building_id = Column(Integer, ForeignKey("buildings.id"))
  sauna_id = Column(Integer, ForeignKey("saunas.id"))

  building = relationship("Building", back_populates="booking")
  sauna = relationship("Sauna", back_populates="booking")
