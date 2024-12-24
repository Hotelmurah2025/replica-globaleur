from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from app.schemas.destination import Destination

class TripDestinationBase(BaseModel):
    destination_id: int
    day_number: int
    order: int
    notes: Optional[str] = None
    start_time: Optional[str] = None  # Format: "HH:MM"
    duration: Optional[int] = None  # Duration in minutes

class TripDestinationCreate(TripDestinationBase):
    pass

class TripDestination(TripDestinationBase):
    id: int
    trip_id: int
    destination: Optional[Destination] = None

    class Config:
        from_attributes = True

class TripBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    is_public: bool = False

class TripCreate(TripBase):
    destinations: List[TripDestinationCreate] = Field(default_factory=list)

class TripUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_public: Optional[bool] = None

class Trip(TripBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    destinations: List[TripDestination] = Field(default_factory=list)

    class Config:
        from_attributes = True

class TripReorder(BaseModel):
    destinations: List[TripDestinationCreate]
