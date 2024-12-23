from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Destination(BaseModel):
    __tablename__ = "destinations"

    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    short_description = Column(String)
    image_url = Column(String)
    images = Column(JSON, default=list)
    latitude = Column(Float)
    longitude = Column(Float)
    country = Column(String, index=True)
    city = Column(String, index=True)
    place_id = Column(String, unique=True, index=True)
    formatted_address = Column(String)
    rating = Column(Float)
    reviews_count = Column(Integer, default=0)
    activities = Column(JSON, default=list)
    price_level = Column(Integer)
    website = Column(String)
    phone_number = Column(String)
    opening_hours = Column(JSON)
    
    reviews = relationship("Review", back_populates="destination")
    trips = relationship("TripDestination", back_populates="destination")
