from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Coordinates(BaseModel):
    lat: float
    lng: float

class LocationBase(BaseModel):
    place_id: str
    name: str
    formatted_address: str
    coordinates: Coordinates
    types: List[str]

class LocationSearch(BaseModel):
    query: str
    language: Optional[str] = "en"  # Support multi-language searches

class LocationSearchResult(LocationBase):
    description: Optional[str] = None
    photo_reference: Optional[str] = None
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None

class LocationDetails(LocationBase):
    description: Optional[str] = None
    photos: List[str] = []
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    website: Optional[str] = None
    formatted_phone_number: Optional[str] = None
    opening_hours: Optional[List[str]] = None
    price_level: Optional[int] = None
    created_at: datetime
    updated_at: datetime
