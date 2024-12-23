from sqlalchemy import Column, String, Integer, ForeignKey, Table, Date, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Trip(BaseModel):
    __tablename__ = "trips"

    title = Column(String, nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_public = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="trips")
    destinations = relationship("TripDestination", back_populates="trip", order_by="TripDestination.day_number, TripDestination.order")

class TripDestination(BaseModel):
    __tablename__ = "trip_destinations"

    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False)
    day_number = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    notes = Column(Text)
    start_time = Column(String)  # Format: "HH:MM"
    duration = Column(Integer)  # Duration in minutes
    
    trip = relationship("Trip", back_populates="destinations")
    destination = relationship("Destination", back_populates="trips")
