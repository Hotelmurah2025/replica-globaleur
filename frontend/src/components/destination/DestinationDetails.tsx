import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { MapView } from '../maps/MapView';
import { ReviewList } from '../reviews/ReviewList';
import { toast } from '../ui/use-toast';

interface Destination {
  id: string;
  name: string;
  description: string;
  images: string[];
  location: {
    lat: number;
    lng: number;
  };
  activities: Array<{
    id: string;
    name: string;
    description: string;
  }>;
}

export function DestinationDetails() {
  const { id } = useParams<{ id: string }>();
  const [destination, setDestination] = useState<Destination | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDestination = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/destinations/${id}`);
        if (!response.ok) {
          throw new Error('Failed to fetch destination details');
        }
        const data = await response.json();
        setDestination(data);
      } catch (error) {
        console.error('Error fetching destination:', error);
        toast({
          title: 'Error',
          description: 'Failed to load destination details',
          variant: 'destructive',
        });
      } finally {
        setIsLoading(false);
      }
    };

    if (id) {
      fetchDestination();
    }
  }, [id]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!destination) {
    return <div>Destination not found</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-6">{destination.name}</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <div className="aspect-video rounded-lg overflow-hidden mb-4">
            {destination.images[0] && (
              <img
                src={destination.images[0]}
                alt={destination.name}
                className="w-full h-full object-cover"
              />
            )}
          </div>
          <p className="text-gray-700 mb-6">{destination.description}</p>
          <div className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Activities</h2>
            <div className="space-y-4">
              {destination.activities.map((activity) => (
                <div key={activity.id} className="p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-medium mb-2">{activity.name}</h3>
                  <p className="text-gray-600">{activity.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="space-y-8">
          <div className="h-[400px]">
            <MapView
              center={destination.location}
              initialLocations={[{
                place_id: destination.id,
                name: destination.name,
                description: '',
                location: destination.location
              }]}
            />
          </div>
          <ReviewList destinationId={destination.id} />
        </div>
      </div>
    </div>
  );
}
