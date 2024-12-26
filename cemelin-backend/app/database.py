from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from .config import settings

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
        logger.debug("=== Starting Database Initialization ===")
        logger.debug(f"Database URL: {SQLALCHEMY_DATABASE_URL}")
        logger.debug(f"SQLAlchemy Base classes: {Base._decl_class_registry.keys()}")
        
        # Import models directly from their modules to avoid circular imports
        from .models.user import User
        from .models.destination import Destination
        from .models.review import Review
        from .models.trip import Trip
        logger.debug("Models imported successfully...")
        models = [User, Destination, Review, Trip]
        logger.debug(f"Available models: {[m.__name__ for m in models]}")
        
        # Drop all tables first to ensure clean state (since we're using in-memory DB)
        logger.debug("Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        logger.debug("Tables dropped successfully")
        
        # Create all tables
        logger.debug("Creating tables...")
        Base.metadata.create_all(bind=engine)
        logger.debug("Base.metadata.create_all() completed")
        
        # Verify tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.debug(f"Tables after creation: {tables}")
        
        if not tables:
            logger.error("No tables were created!")
            raise Exception("No tables were created during initialization")
            
        # Double-check specific tables
        required_tables = ['users', 'destinations', 'reviews', 'trips']
        missing_tables = [table for table in required_tables if table not in tables]
        if missing_tables:
            logger.error(f"Missing tables: {missing_tables}")
            logger.error(f"Available tables: {tables}")
            raise Exception(f"Missing required tables: {missing_tables}")
            
        # Log table details
        for table in tables:
            columns = [col['name'] for col in inspector.get_columns(table)]
            logger.debug(f"Table '{table}' columns: {columns}")
            
        logger.info("=== Database Initialization Complete ===")
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
