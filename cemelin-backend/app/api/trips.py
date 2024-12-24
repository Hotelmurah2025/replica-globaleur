from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.deps import get_db, get_current_user
from app.models.trip import Trip, TripDestination
from app.models.destination import Destination
from app.models.user import User
from app.schemas.trip import (
    TripCreate,
    TripUpdate,
    Trip as TripSchema,
    TripDestinationCreate,
    TripReorder
)

router = APIRouter()

@router.get("/", response_model=List[TripSchema])
def get_user_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """Get all trips for the current user with optional date filtering"""
    query = db.query(Trip).filter(Trip.user_id == current_user.id)
    
    if start_date:
        query = query.filter(Trip.start_date >= start_date)
    if end_date:
        query = query.filter(Trip.end_date <= end_date)
    
    return query.order_by(Trip.start_date.desc()).all()

@router.post("/", response_model=TripSchema)
def create_trip(
    *,
    db: Session = Depends(get_db),
    trip_in: TripCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new trip with destinations"""
    # Validate dates
    if trip_in.end_date < trip_in.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )

    # Create trip
    trip = Trip(
        user_id=current_user.id,
        title=trip_in.title,
        description=trip_in.description,
        start_date=trip_in.start_date,
        end_date=trip_in.end_date,
        is_public=trip_in.is_public
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)

    # Add destinations
    for dest in trip_in.destinations:
        # Verify destination exists
        destination = db.query(Destination).filter(
            Destination.id == dest.destination_id
        ).first()
        if not destination:
            raise HTTPException(
                status_code=404,
                detail=f"Destination {dest.destination_id} not found"
            )
        
        trip_dest = TripDestination(
            trip_id=trip.id,
            destination_id=dest.destination_id,
            day_number=dest.day_number,
            order=dest.order,
            notes=dest.notes,
            start_time=dest.start_time,
            duration=dest.duration
        )
        db.add(trip_dest)
    
    db.commit()
    db.refresh(trip)
    return trip

@router.get("/{trip_id}", response_model=TripSchema)
def get_trip(
    *,
    db: Session = Depends(get_db),
    trip_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get a specific trip"""
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.put("/{trip_id}", response_model=TripSchema)
def update_trip(
    *,
    db: Session = Depends(get_db),
    trip_id: int,
    trip_in: TripUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update trip details"""
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Validate dates if both are provided
    if trip_in.start_date and trip_in.end_date: 
        if trip_in.end_date < trip_in.start_date:
            raise HTTPException(
                status_code=400,
                detail="End date cannot be before start date"
            )
    
    update_data = trip_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(trip, field, value)
    
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip

@router.delete("/{trip_id}")
def delete_trip(
    *,
    db: Session = Depends(get_db),
    trip_id: int,
    current_user: User = Depends(get_current_user)
):
    """Delete a trip"""
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted successfully"}

@router.put("/{trip_id}/reorder", response_model=TripSchema)
def reorder_trip_destinations(
    *,
    db: Session = Depends(get_db),
    trip_id: int,
    reorder_data: TripReorder,
    current_user: User = Depends(get_current_user)
):
    """Reorder destinations within a trip"""
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Delete existing destinations
    db.query(TripDestination).filter(TripDestination.trip_id == trip_id).delete()
    
    # Add destinations in new order
    for dest in reorder_data.destinations:
        trip_dest = TripDestination(
            trip_id=trip_id,
            destination_id=dest.destination_id,
            day_number=dest.day_number,
            order=dest.order,
            notes=dest.notes,
            start_time=dest.start_time,
            duration=dest.duration
        )
        db.add(trip_dest)
    
    db.commit()
    db.refresh(trip)
    return trip
