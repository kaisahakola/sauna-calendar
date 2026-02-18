from models import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Sauna(Base):
  __tablename__ = "saunas"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  building_id = Column(Integer, ForeignKey("buildings.id"))

  building = relationship("Building", back_populates="sauna")
