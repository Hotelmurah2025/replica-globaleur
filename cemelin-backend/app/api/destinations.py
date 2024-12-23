from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.deps import get_db, get_current_user
from app.models.destination import Destination
from app.models.user import User
from app.schemas.destination import DestinationCreate, Destination as DestinationSchema, DestinationSearch

router = APIRouter()

@router.get("/search", response_model=List[DestinationSchema])
def search_destinations(
    *,
    db: Session = Depends(get_db),
    query: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100)
):
    destinations = db.query(Destination).filter(
        Destination.name.ilike(f"%{query}%")
    ).limit(limit).all()
    return destinations

@router.get("/{destination_id}", response_model=DestinationSchema)
def get_destination(*, db: Session = Depends(get_db), destination_id: int):
    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination

@router.post("/", response_model=DestinationSchema)
def create_destination(
    *,
    db: Session = Depends(get_db),
    destination_in: DestinationCreate,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    destination = Destination(**destination_in.model_dump())
    db.add(destination)
    db.commit()
    db.refresh(destination)
    return destination
