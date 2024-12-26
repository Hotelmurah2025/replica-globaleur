from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, Base, engine
from app.deps import get_settings  # Import deps before api modules
from app.api import auth, destinations, reviews, trips, contact, i18n, locations, maps
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://travel-destination-app-75inxnsu.devinapps.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin"]
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(destinations.router, prefix=f"{settings.API_V1_STR}/destinations", tags=["destinations"])
app.include_router(reviews.router, prefix=f"{settings.API_V1_STR}/reviews", tags=["reviews"])
app.include_router(trips.router, prefix=f"{settings.API_V1_STR}/trips", tags=["trips"])
app.include_router(contact.router, prefix=f"{settings.API_V1_STR}/contact", tags=["contact"])
app.include_router(i18n.router, prefix=f"{settings.API_V1_STR}/i18n", tags=["i18n"])
app.include_router(locations.router, prefix=f"{settings.API_V1_STR}/locations", tags=["locations"])
app.include_router(maps.router, prefix=f"{settings.API_V1_STR}/maps", tags=["maps"])

@app.on_event("startup")
async def startup_event():
    """Initialize database and create all tables on application startup."""
    try:
        # Import all models to ensure they're registered
        from app.models import user, destination, review, trip
        from app.database import init_db, engine, Base
        from sqlalchemy import inspect
        
        logger.info("Starting database initialization...")
        logger.info(f"Using database URL: {settings.DATABASE_URL}")
        
        # Drop all tables first to ensure clean state (since we're using in-memory DB)
        logger.info("Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        
        # Initialize database and create tables
        logger.info("Initializing database...")
        init_db()
        
        # Verify tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Created tables: {tables}")
        
        if not tables:
            raise Exception("No tables were created during initialization")
            
        logger.info("Database initialized successfully on startup")
    except Exception as e:
        logger.error(f"Failed to initialize database on startup: {e}")
        raise

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
