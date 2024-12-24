import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { MapView } from '../components/maps/MapView';
import { Loader2 } from 'lucide-react';

/// <reference types="vite/client" />

interface Destination {
  id: string;
  name: string;
  description: string;
  location: {
    lat: number;
    lng: number;
  };
  images: string[];
  activities: {
    name: string;
    description: string;
  }[];
}

export function DestinationDetails() {
  const { t } = useTranslation();
  const { id } = useParams();
  const [destination, setDestination] = useState<Destination | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDestination = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/destinations/${id}`);
        if (response.ok) {
          const data = await response.json();
          setDestination(data);
        }
      } catch (error) {
        console.error('Failed to fetch destination:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDestination();
  }, [id]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (!destination) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-semibold text-gray-900">
          {t('destinations.notFound')}
        </h1>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>{`${destination.name} - Cemelin Travel`}</title>
        <meta name="description" content={destination.description} />
      </Helmet>

      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-6">
          {destination.name}
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div>
            {destination.images.length > 0 && (
              <img
                src={destination.images[0]}
                alt={destination.name}
                className="w-full h-96 object-cover rounded-lg shadow-lg"
              />
            )}
          </div>
          <div>
            <p className="text-lg text-gray-700 mb-6">
              {destination.description}
            </p>
            <MapView
              center={destination.location}
              markers={[destination.location]}
            />
          </div>
        </div>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            {t('destinations.recommendedActivities')}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {destination.activities.map((activity, index) => (
              <div
                key={index}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
              >
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {activity.name}
                </h3>
                <p className="text-gray-700">{activity.description}</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </>
  );
}
