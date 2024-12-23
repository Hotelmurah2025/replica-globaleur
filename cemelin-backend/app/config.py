from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cemelin Travel API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-for-jwt"  # In production, this should be in .env
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Google Places API configuration
    google_places_api_key: Optional[str] = None
    
    # Rate limiting settings
    rate_limit_requests: int = 100  # Number of requests
    rate_limit_period: int = 60  # Time period in seconds

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
