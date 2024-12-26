from .user import User
from .destination import Destination
from .review import Review
from .trip import Trip

# Import all models here to ensure they are registered with SQLAlchemy Base
__all__ = [
    "User",
    "Destination",
    "Review",
    "Trip"
]
