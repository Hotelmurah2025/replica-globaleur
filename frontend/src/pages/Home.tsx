import { useState } from 'react';
import { useLoadScript } from '@react-google-maps/api';
import { SearchBox } from '@/components/search/SearchBox';
import { MapView } from '@/components/maps/MapView';
import { useTranslation } from 'react-i18next';

const libraries: ("places")[] = ["places"];

const Home = () => {
  const { t } = useTranslation();
  const [selectedPlace, setSelectedPlace] = useState<google.maps.places.PlaceResult | null>(null);
  const [mapCenter, setMapCenter] = useState<google.maps.LatLngLiteral>({
    lat: -6.200000,  // Jakarta's latitude
    lng: 106.816666  // Jakarta's longitude
  });

  const { isLoaded } = useLoadScript({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || '',
    libraries,
  });

  const handlePlaceSelect = (place: google.maps.places.PlaceResult) => {
    if (place.geometry?.location) {
      setSelectedPlace(place);
      setMapCenter({
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng(),
      });
    }
  };

  if (!isLoaded) return <div>Loading...</div>;

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative h-96 bg-gradient-to-r from-blue-600 to-blue-400 flex items-center justify-center">
        <div className="container text-center text-white">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            {t('hero.title')}
          </h1>
          <p className="text-xl mb-8">
            {t('hero.subtitle')}
          </p>
          
          {/* Search Bar */}
          <SearchBox onPlaceSelect={handlePlaceSelect} />
        </div>
      </div>

      {/* Map Section */}
      <div className="container mx-auto px-4 py-8">
        <div className="mb-12">
          <MapView 
            center={mapCenter}
            markers={selectedPlace?.geometry?.location ? [mapCenter] : []}
          />
        </div>

        {/* Popular Destinations */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div className="p-6 bg-white rounded-lg shadow-md transition-transform hover:scale-105">
            <h3 className="text-xl font-semibold mb-2">{t('home.popularDestinations')}</h3>
            <p className="text-gray-600">{t('home.exploreLocations')}</p>
          </div>
          <div className="p-6 bg-white rounded-lg shadow-md transition-transform hover:scale-105">
            <h3 className="text-xl font-semibold mb-2">{t('home.planTrip')}</h3>
            <p className="text-gray-600">{t('home.createItinerary')}</p>
          </div>
          <div className="p-6 bg-white rounded-lg shadow-md transition-transform hover:scale-105">
            <h3 className="text-xl font-semibold mb-2">{t('home.reviews')}</h3>
            <p className="text-gray-600">{t('home.readExperiences')}</p>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Home;
