from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TripBase(BaseModel):
    title: str

class TripCreate(TripBase):
    destination_ids: List[int]

class TripDestinationBase(BaseModel):
    destination_id: int
    order: int

class Trip(TripBase):
    id: int
    user_id: int
    created_at: datetime
    destinations: List[TripDestinationBase]
    
    class Config:
        from_attributes = True
