from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Activity(BaseModel):
    name: str
    description: str
    duration: Optional[str] = None
    price_range: Optional[str] = None

class OpeningHours(BaseModel):
    weekday_text: List[str] = Field(default_factory=list)
    periods: List[Dict] = Field(default_factory=list)

class DestinationBase(BaseModel):
    name: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    image_url: Optional[str] = None
    images: List[str] = Field(default_factory=list)
    latitude: float
    longitude: float
    country: str
    city: str
    place_id: str
    formatted_address: str
    rating: Optional[float] = None
    reviews_count: Optional[int] = 0
    activities: List[Activity] = Field(default_factory=list)
    price_level: Optional[int] = None
    website: Optional[str] = None
    phone_number: Optional[str] = None
    opening_hours: Optional[OpeningHours] = None

class DestinationCreate(DestinationBase):
    pass

class Destination(DestinationBase):
    id: int
    
    class Config:
        from_attributes = True

class DestinationSearch(BaseModel):
    query: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius: Optional[int] = 50000  # Default 50km radius
    limit: Optional[int] = 10

class PlaceDetails(BaseModel):
    place_id: str
    name: str
    formatted_address: str
    geometry: Dict[str, Dict[str, float]]
    rating: Optional[float] = None
    photos: List[str] = Field(default_factory=list)
    opening_hours: Optional[OpeningHours] = None
    price_level: Optional[int] = None
    website: Optional[str] = None
    formatted_phone_number: Optional[str] = None
