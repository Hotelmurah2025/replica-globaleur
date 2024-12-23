from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Trip(BaseModel):
    __tablename__ = "trips"

    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User")
    destinations = relationship("TripDestination", back_populates="trip")

class TripDestination(BaseModel):
    __tablename__ = "trip_destinations"

    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    order = Column(Integer, nullable=False)
    
    trip = relationship("Trip", back_populates="destinations")
    destination = relationship("Destination", back_populates="trips")
