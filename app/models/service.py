from sqlalchemy import Column, Integer, String, Float
from app.db.base_class import Base

class Service(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)