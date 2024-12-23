import { useState, useCallback } from 'react';
import { GoogleMap, Marker, LoadScript } from '@react-google-maps/api';
import { Loader2 } from 'lucide-react';

const containerStyle = {
  width: '100%',
  height: '500px'
};

const defaultCenter = {
  lat: -6.200000,  // Jakarta's latitude
  lng: 106.816666  // Jakarta's longitude
};

interface MapViewProps {
  center?: google.maps.LatLngLiteral;
  markers?: google.maps.LatLngLiteral[];
}

export function MapView({ center = defaultCenter, markers = [] }: MapViewProps) {
  const [isLoading, setIsLoading] = useState(true);

  const onLoad = useCallback(() => {
    setIsLoading(false);
  }, []);

  const onUnmount = useCallback(() => {
    setIsLoading(true);
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
        {markers.map((position, idx) => (
          <Marker key={idx} position={position} />
        ))}
      </GoogleMap>
      </LoadScript>
    </div>
  );
}
