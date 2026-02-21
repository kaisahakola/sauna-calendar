from models.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Building(Base):
  __tablename__ = "buildings"
  id = Column(Integer, primary_key=True)
  address = Column(String)
  name = Column(String)

  user = relationship("User", back_populates="building", order_by="User.id")
  sauna = relationship("Sauna", back_populates="building", cascade="all, delete")
  booking = relationship("Booking", back_populates="building")
