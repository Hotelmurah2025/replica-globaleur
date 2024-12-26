from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import logging

from .config import settings
from .models.base import Base, metadata

logger = logging.getLogger(__name__)

# Get database URL from settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database and create all tables."""
    try:
        # Import models package first to ensure all models are registered
        from . import models
        logger.debug("Models imported successfully")
        
        # Drop all tables first to ensure clean state (since we're using in-memory DB)
        Base.metadata.drop_all(bind=engine)
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        # Check required tables
        required_tables = ['users', 'destinations', 'reviews', 'trips']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            raise Exception(f"Missing required tables: {missing_tables}")
            
        logger.info(f"Successfully created tables: {tables}")
        return True
    except Exception as e:
        logger.error("=== Database Initialization Failed ===")
        logger.error(f"Error details: {str(e)}")
        logger.exception("Full traceback:")
        raise

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
