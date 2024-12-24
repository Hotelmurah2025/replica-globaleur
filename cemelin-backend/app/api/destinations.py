from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import googlemaps
from app.deps import get_db, get_current_user
from app.models.destination import Destination
from app.models.user import User
from app.schemas.destination import (
    DestinationCreate,
    Destination as DestinationSchema,
    DestinationSearch,
    PlaceDetails,
    Activity
)
from app.config import settings

router = APIRouter()
gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

@router.get("/search", response_model=List[PlaceDetails])
async def search_destinations(
    *,
    db: Session = Depends(get_db),
    query: str = Query(..., min_length=1),
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: Optional[int] = 50000,
    limit: int = Query(10, ge=1, le=20)
):
    try:
        # Search using Google Places API
        location = None if latitude is None or longitude is None else {"lat": latitude, "lng": longitude}
        places_result = gmaps.places(
            query,
            location=location,
            radius=radius,
            language="en",
            type="tourist_attraction"
        )

        results = []
        for place in places_result.get("results", [])[:limit]:
            # Get detailed place information
            place_details = gmaps.place(
                place["place_id"],
                fields=["name", "formatted_address", "geometry", "rating", "photos",
                       "opening_hours", "price_level", "website", "formatted_phone_number"]
            )["result"]

            # Get photo URLs if available
            photos = []
            if "photos" in place_details:
                for photo in place_details["photos"][:5]:  # Limit to 5 photos
                    try:
                        photo_url = gmaps.places_photo(
                            photo["photo_reference"],
                            max_width=800
                        )
                        photos.append(photo_url)
                    except Exception:
                        continue

            result = PlaceDetails(
                place_id=place["place_id"],
                name=place["name"],
                formatted_address=place["formatted_address"],
                geometry=place["geometry"],
                rating=place_details.get("rating"),
                photos=photos,
                opening_hours=place_details.get("opening_hours"),
                price_level=place_details.get("price_level"),
                website=place_details.get("website"),
                formatted_phone_number=place_details.get("formatted_phone_number")
            )
            results.append(result)

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{place_id}", response_model=DestinationSchema)
async def get_destination(
    *,
    db: Session = Depends(get_db),
    place_id: str
):
    # First check if destination exists in database
    destination = db.query(Destination).filter(Destination.place_id == place_id).first()
    
    if not destination:
        try:
            # Get place details from Google Places API
            place_details = gmaps.place(
                place_id,
                fields=["name", "formatted_address", "geometry", "rating", "photos",
                       "opening_hours", "price_level", "website", "formatted_phone_number",
                       "reviews", "address_components"]
            )["result"]

            # Extract country and city from address components
            country = ""
            city = ""
            for component in place_details.get("address_components", []):
                if "country" in component["types"]:
                    country = component["long_name"]
                elif "locality" in component["types"]:
                    city = component["long_name"]

            # Create new destination
            destination = Destination(
                name=place_details["name"],
                description="",  # To be filled by admin
                short_description="",  # To be filled by admin
                place_id=place_id,
                formatted_address=place_details["formatted_address"],
                latitude=place_details["geometry"]["location"]["lat"],
                longitude=place_details["geometry"]["location"]["lng"],
                country=country,
                city=city,
                rating=place_details.get("rating"),
                reviews_count=len(place_details.get("reviews", [])),
                price_level=place_details.get("price_level"),
                website=place_details.get("website"),
                phone_number=place_details.get("formatted_phone_number"),
                opening_hours=place_details.get("opening_hours"),
                activities=[]  # To be filled by admin
            )

            # Get photos
            if "photos" in place_details:
                photos = []
                for photo in place_details["photos"][:5]:
                    try:
                        photo_url = gmaps.places_photo(
                            photo["photo_reference"],
                            max_width=800
                        )
                        photos.append(photo_url)
                    except Exception:
                        continue
                destination.images = photos
                if photos:
                    destination.image_url = photos[0]

            db.add(destination)
            db.commit()
            db.refresh(destination)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return destination

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
