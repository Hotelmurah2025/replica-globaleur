from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=False)  # Default to False until email is verified
    is_superuser = Column(Boolean, default=False)
    
    # Email verification
    verification_token = Column(String, unique=True, nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
    
    # Password reset
    reset_token = Column(String, unique=True, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    
    # Timestamps
    last_login = Column(DateTime, nullable=True)
    password_changed_at = Column(DateTime, nullable=True)
    
    # Relationships
    trips = relationship("Trip", back_populates="user")
