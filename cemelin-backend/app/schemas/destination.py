from pydantic import BaseModel
from typing import Optional, List

class DestinationBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    country: str
    city: str

class DestinationCreate(DestinationBase):
    pass

class Destination(DestinationBase):
    id: int
    
    class Config:
        from_attributes = True

class DestinationSearch(BaseModel):
    query: str
    limit: Optional[int] = 10
