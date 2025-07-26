from sqlalchemy import Column, Integer, String, Float
from app.models.base import Base

class DistributionCenter(Base):
    __tablename__ = 'distribution_centers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float) 