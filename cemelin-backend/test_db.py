from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.destination import Destination
from app.models.review import Review
from app.models.trip import Trip

def test_database():
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created successfully")
        
        # Test session creation
        db = SessionLocal()
        try:
            # Try a simple query
            result = db.query(User).first()
            print("✓ Database connection successful")
            print("✓ Available tables:", list(Base.metadata.tables.keys()))
        finally:
            db.close()
            print("✓ Database session closed properly")
            
        return True
    except Exception as e:
        print("✗ Database initialization failed:")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing database initialization...")
    success = test_database()
    if success:
        print("\nDatabase initialization completed successfully! ✨")
    else:
        print("\nDatabase initialization failed! ❌")
