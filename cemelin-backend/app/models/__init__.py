from .base import Base
from .user import User
from .destination import Destination
from .review import Review
from .trip import Trip

# Import all models here to ensure they are registered with SQLAlchemy Base
__all__ = [
    "Base",
    "User",
    "Destination",
    "Review",
    "Trip"
]

# Create a list of all models for database initialization
all_models = [User, Destination, Review, Trip]
