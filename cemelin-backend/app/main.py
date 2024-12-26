import logging
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, engine
from app.models.base import Base
from app.deps import get_settings  # Import deps before api modules

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True,  # Force reconfiguration
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.StreamHandler(sys.stderr)
    ]
)

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Configure app logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Configure SQLAlchemy logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

# Initialize database before creating FastAPI app
logger.info("Initializing database before application startup...")
init_db()

# Import routers after database initialization
from app.api import auth, destinations, reviews, trips, contact, i18n, locations, maps

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
    """Verify database initialization on application startup."""
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Available tables at startup: {tables}")
        if not tables:
            raise Exception("No tables found in database at startup")
        logger.info("Database verification completed successfully")
    except Exception as e:
        logger.error(f"Database verification failed on startup: {e}")
        raise

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
