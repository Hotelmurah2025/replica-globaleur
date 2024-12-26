from sqlalchemy import create_engine, inspect
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
        logger.info("Starting database initialization...")
        logger.info(f"Using database URL: {SQLALCHEMY_DATABASE_URL}")
        
        # Drop all tables first to ensure clean state (since we're using in-memory DB)
        logger.info("Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        
        # Import all models to ensure they're registered
        from app.models import user, destination, review, trip
        
        # Create all tables
        logger.info("Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        # Verify tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Created tables: {tables}")
        
        if not tables:
            raise Exception("No tables were created during initialization")
            
        logger.info("Database tables created successfully")
        return True
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
