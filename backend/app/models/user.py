from models import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  email = Column(String)
  role = Column(String)
  building_id = Column(Integer, ForeignKey("buildings.id"))

  building = relationship("Building", back_populates="user")
