from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.deps import get_db, get_current_user
from app.models.trip import Trip, TripDestination
from app.models.user import User
from app.schemas.trip import TripCreate, Trip as TripSchema

router = APIRouter()

@router.get("/", response_model=List[TripSchema])
def get_user_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Trip).filter(Trip.user_id == current_user.id).all()

@router.post("/", response_model=TripSchema)
def create_trip(
    *,
    db: Session = Depends(get_db),
    trip_in: TripCreate,
    current_user: User = Depends(get_current_user)
):
    trip = Trip(title=trip_in.title, user_id=current_user.id)
    db.add(trip)
    db.commit()
    db.refresh(trip)
    
    for idx, dest_id in enumerate(trip_in.destination_ids):
        trip_dest = TripDestination(
            trip_id=trip.id,
            destination_id=dest_id,
            order=idx
        )
        db.add(trip_dest)
    
    db.commit()
    db.refresh(trip)
    return trip
