from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, declared_attr, MappedAsDataclass
from typing import Any

class Base(DeclarativeBase):
    """Base class for all models"""
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class BaseModel(Base):
    """Base model class that includes common fields"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
