from app.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Sauna(Base):
  __tablename__ = "saunas"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  building_id = Column(Integer, ForeignKey("buildings.id", ondelete="CASCADE"), nullable=True)

  building = relationship("Building", back_populates="sauna")
  booking = relationship("Booking", back_populates="sauna", cascade="all, delete")
