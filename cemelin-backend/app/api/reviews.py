from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.deps import get_db, get_current_user
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, Review as ReviewSchema

router = APIRouter()

@router.get("/destination/{destination_id}", response_model=List[ReviewSchema])
def get_destination_reviews(
    destination_id: int,
    db: Session = Depends(get_db)
):
    reviews = db.query(Review).filter(Review.destination_id == destination_id).all()
    return reviews

@router.post("/", response_model=ReviewSchema)
def create_review(
    *,
    db: Session = Depends(get_db),
    review_in: ReviewCreate,
    current_user: User = Depends(get_current_user)
):
    review = Review(
        **review_in.model_dump(),
        user_id=current_user.id
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
