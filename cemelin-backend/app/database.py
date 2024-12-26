from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from .config import settings
from .models import user, destination, review, trip  # Import all models

logger = logging.getLogger(__name__)

# Get database URL from settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """Initialize database and create all tables."""
    try:
        # Import all models to ensure they're registered with SQLAlchemy
        from .models import user, destination, review, trip
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
