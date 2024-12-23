from pydantic import BaseModel, conint
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    rating: conint(ge=1, le=5)  # Rating between 1 and 5
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    destination_id: int

class Review(ReviewBase):
    id: int
    user_id: int
    destination_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
