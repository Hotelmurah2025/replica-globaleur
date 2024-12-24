from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALLOWED_ORIGINS: str
    DATABASE_URL: str
    
    # Google Places API configuration
    GOOGLE_PLACES_API_KEY: str
    
    # Rate limiting settings
    rate_limit_requests: int = 100  # Number of requests
    rate_limit_period: int = 60  # Time period in seconds

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()
