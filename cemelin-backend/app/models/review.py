from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Review(BaseModel):
    __tablename__ = "reviews"

    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)

    user = relationship("User")
    destination = relationship("Destination", back_populates="reviews")
