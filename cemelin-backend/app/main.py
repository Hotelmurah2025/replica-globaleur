from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, destinations, reviews, trips, contact
from app.config import settings
from app.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(destinations.router, prefix=f"{settings.API_V1_STR}/destinations", tags=["destinations"])
app.include_router(reviews.router, prefix=f"{settings.API_V1_STR}/reviews", tags=["reviews"])
app.include_router(trips.router, prefix=f"{settings.API_V1_STR}/trips", tags=["trips"])
app.include_router(contact.router, prefix=f"{settings.API_V1_STR}/contact", tags=["contact"])

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
