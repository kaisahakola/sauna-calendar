from app.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  email = Column(String)
  role = Column(String)
  building_id = Column(Integer, ForeignKey("buildings.id", ondelete="SET NULL"), nullable=True)

  building = relationship("Building", back_populates="user")
  booking = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
