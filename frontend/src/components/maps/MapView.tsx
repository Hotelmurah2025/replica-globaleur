import { useState, useCallback } from 'react';
import { GoogleMap, Marker, LoadScript } from '@react-google-maps/api';
import { Loader2 } from 'lucide-react';
import { toast } from '@/components/ui/use-toast';

const containerStyle = {
  width: '100%',
  height: '500px'
};

const defaultCenter = {
  lat: -6.200000,  // Jakarta's latitude
  lng: 106.816666  // Jakarta's longitude
};

interface Location {
  place_id: string;
  name: string;
  description: string;
  location: {
    lat: number;
    lng: number;
  };
}

interface MapMarker {
  place_id: string;
  title: string;
  lat: number;
  lng: number;
}

interface MapViewProps {
  center?: { lat: number; lng: number };
  initialLocations?: Location[];
  markers?: { lat: number; lng: number }[];
}

export function MapView({ center = defaultCenter, initialLocations = [] }: MapViewProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [markers, setMarkers] = useState<MapMarker[]>(
    initialLocations.map(loc => ({
      place_id: loc.place_id,
      title: loc.name,
      lat: loc.location.lat,
      lng: loc.location.lng
    }))
  );

  const fetchNearbyMarkers = useCallback(async (mapCenter: { lat: number; lng: number }) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/maps/markers`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          center: mapCenter,
          radius: 5000, // 5km radius
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch markers');
      }

      const data = await response.json();
      setMarkers(prevMarkers => {
        const newMarkers = data.map((m: { place_id: string; name: string; location: { lat: number; lng: number } }) => ({
          place_id: m.place_id,
          title: m.name,
          lat: m.location.lat,
          lng: m.location.lng,
        }));
        return [...prevMarkers, ...newMarkers];
      });
    } catch (error) {
      console.error('Error fetching markers:', error);
      toast({
        title: 'Error',
        description: 'Failed to load nearby locations',
        variant: 'destructive',
      });
    }
  }, []);

  const onLoad = useCallback(() => {
    setIsLoading(false);
    fetchNearbyMarkers(center);
  }, [center, fetchNearbyMarkers]);

  const onUnmount = useCallback(() => {
    setIsLoading(true);
    setMarkers([]);
  }, []);

  return (
    <div className="w-full rounded-lg overflow-hidden shadow-lg relative">
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100 z-10">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        </div>
      )}
      <LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
        <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={10}
        onLoad={onLoad}
        onUnmount={onUnmount}
        options={{
          zoomControl: true,
          streetViewControl: false,
          mapTypeControl: false,
          fullscreenControl: false,
        }}
      >
        {markers.map((marker) => (
          <Marker
            key={marker.place_id}
            position={{ lat: marker.lat, lng: marker.lng }}
            title={marker.title}
          />
        ))}
      </GoogleMap>
      </LoadScript>
    </div>
  );
}
