from sqlalchemy import Column, Integer, DateTime, MetaData
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, declared_attr, registry
from typing import Any

# Create a new registry with naming convention
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
mapper_registry = registry(metadata=metadata)

class Base(DeclarativeBase):
    """Base class for all models"""
    metadata = metadata
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class BaseModel(Base):
    """Base model class that includes common fields"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
