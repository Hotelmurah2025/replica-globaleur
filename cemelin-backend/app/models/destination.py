from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Destination(BaseModel):
    __tablename__ = "destinations"

    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    image_url = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    country = Column(String, index=True)
    city = Column(String, index=True)
    
    reviews = relationship("Review", back_populates="destination")
    trips = relationship("TripDestination", back_populates="destination")
