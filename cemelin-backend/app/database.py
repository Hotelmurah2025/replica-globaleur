from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import logging

from .config import settings
from .models.base import metadata

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
        logger.info("Starting database initialization...")
        
        # Import Base and models to ensure proper registration
        from .models.base import Base
        from .models import user, destination, review, trip
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        # Check required tables
        required_tables = ['users', 'destinations', 'reviews', 'trips']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            logger.error(f"Missing required tables: {missing_tables}")
            raise Exception(f"Database initialization failed: missing tables {missing_tables}")
            
        logger.info(f"Database initialized successfully with tables: {tables}")
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
