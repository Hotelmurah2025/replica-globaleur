from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.deps import get_settings  # Import deps before api modules
from app.api import auth, destinations, reviews, trips, contact, i18n, locations, maps
import logging

logger = logging.getLogger(__name__)

# Create database tables
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

# Initialize database on startup
init_db()

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

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
