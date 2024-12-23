from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import httpx
from app.deps import get_db, get_settings
from app.schemas.location import LocationSearch, LocationSearchResult, LocationDetails, Coordinates
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/search", response_model=List[LocationSearchResult])
async def search_locations(
    *,
    db: Session = Depends(get_db),
    settings = Depends(get_settings),
    query: str = Query(..., min_length=2),
    language: str = Query("en", regex="^(en|id)$")  # Only allow English and Indonesian
):
    """
    Search for locations using Google Places API with autocomplete support.
    """
    try:
        if not settings.google_places_api_key:
            raise HTTPException(
                status_code=500,
                detail="Google Places API key not configured"
            )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/place/autocomplete/json",
                params={
                    "input": query,
                    "key": settings.google_places_api_key,
                    "language": language,
                    "types": "(cities)"  # Focus on cities for travel destinations
                }
            )
            response.raise_for_status()
            data = response.json()

            if data["status"] != "OK":
                logger.error(f"Google Places API error: {data['status']}")
                raise HTTPException(
                    status_code=500,
                    detail="Error fetching location suggestions"
                )

            # Get details for each place
            results = []
            for prediction in data["predictions"]:
                place_id = prediction["place_id"]
                details_response = await client.get(
                    "https://maps.googleapis.com/maps/api/place/details/json",
                    params={
                        "place_id": place_id,
                        "key": settings.google_places_api_key,
                        "language": language,
                        "fields": "name,formatted_address,geometry,type,photos,rating,user_ratings_total"
                    }
                )
                details_response.raise_for_status()
                place_data = details_response.json()

                if place_data["status"] == "OK":
                    place = place_data["result"]
                    results.append(LocationSearchResult(
                        place_id=place_id,
                        name=place["name"],
                        formatted_address=place["formatted_address"],
                        coordinates=Coordinates(
                            lat=place["geometry"]["location"]["lat"],
                            lng=place["geometry"]["location"]["lng"]
                        ),
                        types=place.get("types", []),
                        photo_reference=place.get("photos", [{}])[0].get("photo_reference"),
                        rating=place.get("rating"),
                        user_ratings_total=place.get("user_ratings_total")
                    ))

            return results

    except httpx.RequestError as e:
        logger.error(f"Error making request to Google Places API: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error connecting to location service"
        )
    except Exception as e:
        logger.error(f"Unexpected error in location search: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.get("/{place_id}", response_model=LocationDetails)
async def get_location_details(
    *,
    db: Session = Depends(get_db),
    settings = Depends(get_settings),
    place_id: str,
    language: str = Query("en", regex="^(en|id)$")
):
    """
    Get detailed information about a specific location.
    """
    try:
        if not settings.google_places_api_key:
            raise HTTPException(
                status_code=500,
                detail="Google Places API key not configured"
            )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/place/details/json",
                params={
                    "place_id": place_id,
                    "key": settings.google_places_api_key,
                    "language": language,
                    "fields": "name,formatted_address,geometry,type,photos,rating,user_ratings_total,website,formatted_phone_number,opening_hours,price_level"
                }
            )
            response.raise_for_status()
            data = response.json()

            if data["status"] != "OK":
                logger.error(f"Google Places API error: {data['status']}")
                raise HTTPException(
                    status_code=404 if data["status"] == "ZERO_RESULTS" else 500,
                    detail="Location not found" if data["status"] == "ZERO_RESULTS" else "Error fetching location details"
                )

            place = data["result"]
            photos = []
            if "photos" in place:
                for photo in place["photos"][:5]:  # Limit to 5 photos
                    photo_response = await client.get(
                        "https://maps.googleapis.com/maps/api/place/photo",
                        params={
                            "maxwidth": 800,
                            "photo_reference": photo["photo_reference"],
                            "key": settings.google_places_api_key
                        }
                    )
                    if photo_response.status_code == 200:
                        photos.append(photo_response.url)

            return LocationDetails(
                place_id=place_id,
                name=place["name"],
                formatted_address=place["formatted_address"],
                coordinates=Coordinates(
                    lat=place["geometry"]["location"]["lat"],
                    lng=place["geometry"]["location"]["lng"]
                ),
                types=place.get("types", []),
                photos=photos,
                rating=place.get("rating"),
                user_ratings_total=place.get("user_ratings_total"),
                website=place.get("website"),
                formatted_phone_number=place.get("formatted_phone_number"),
                opening_hours=place.get("opening_hours", {}).get("weekday_text", []),
                price_level=place.get("price_level"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

    except httpx.RequestError as e:
        logger.error(f"Error making request to Google Places API: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error connecting to location service"
        )
    except Exception as e:
        logger.error(f"Unexpected error in location details: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
