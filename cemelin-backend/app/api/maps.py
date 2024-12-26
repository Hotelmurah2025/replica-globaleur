from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.schemas.location import Coordinates, MapMarker, MapBounds
from app.config import settings
import httpx

router = APIRouter()

@router.post("/markers", response_model=List[MapMarker])
async def get_location_markers(bounds: MapBounds):
    """
    Get location markers within the specified map bounds.
    This endpoint is used for displaying pins on the map interface.
    """
    if not settings.google_maps_api_key:
        raise HTTPException(
            status_code=500,
            detail="Google Maps API key not configured"
        )
    
    try:
        async with httpx.AsyncClient() as client:
            # Use the Places API to search for places within the bounds
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                "key": settings.google_maps_api_key,
                "location": f"{bounds.center.lat},{bounds.center.lng}",
                "radius": bounds.radius,  # in meters
                "type": "tourist_attraction"
            }
            
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                raise HTTPException(
                    status_code=400,
                    detail=f"Google Places API error: {data.get('status')}"
                )
            
            markers = []
            for result in data.get("results", []):
                location = result.get("geometry", {}).get("location", {})
                markers.append(MapMarker(
                    lat=location.get("lat"),
                    lng=location.get("lng"),
                    title=result.get("name"),
                    place_id=result.get("place_id"),
                    rating=result.get("rating"),
                    icon=result.get("icon")
                ))
            
            return markers
            
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching location markers: {str(e)}"
        )

@router.get("/static-map/{place_id}", response_model=str)
async def get_static_map_url(place_id: str, width: int = 600, height: int = 400, zoom: int = 15):
    """
    Generate a static map URL for a specific location.
    This is useful for generating map previews in the UI.
    """
    if not settings.google_maps_api_key:
        raise HTTPException(
            status_code=500,
            detail="Google Maps API key not configured"
        )
    
    try:
        async with httpx.AsyncClient() as client:
            # First, get the place details to get coordinates
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                "key": settings.google_maps_api_key,
                "place_id": place_id,
                "fields": "geometry"
            }
            
            response = await client.get(details_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                raise HTTPException(
                    status_code=400,
                    detail=f"Google Places API error: {data.get('status')}"
                )
            
            location = data.get("result", {}).get("geometry", {}).get("location", {})
            if not location:
                raise HTTPException(
                    status_code=404,
                    detail="Location not found"
                )
            
            # Generate static map URL
            static_map_url = (
                f"https://maps.googleapis.com/maps/api/staticmap?"
                f"center={location.get('lat')},{location.get('lng')}&"
                f"zoom={zoom}&size={width}x{height}&"
                f"markers=color:red%7C{location.get('lat')},{location.get('lng')}&"
                f"key={settings.google_maps_api_key}"
            )
            
            return static_map_url
            
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating static map: {str(e)}"
        )
