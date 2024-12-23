import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Search, Loader2 } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { toast } from '@/components/ui/use-toast';

interface SearchBoxProps {
  onPlaceSelect?: (place: google.maps.places.PlaceResult) => void;
}

export function SearchBox({ onPlaceSelect }: SearchBoxProps) {
  const { t } = useTranslation();
  const [searchInput, setSearchInput] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [autocomplete, setAutocomplete] = useState<google.maps.places.Autocomplete | null>(null);

  useEffect(() => {
    const initAutocomplete = () => {
      if (!window.google || !window.google.maps) {
        toast({
          title: t('search.error'),
          description: t('search.googleMapsError'),
          variant: "destructive",
        });
        setIsLoading(false);
        return;
      }

      if (!autocomplete) {
        const autocompleteInstance = new google.maps.places.Autocomplete(
          document.getElementById('location-search') as HTMLInputElement,
          { types: ['geocode'] }
        );

        autocompleteInstance.addListener('place_changed', () => {
          const place = autocompleteInstance.getPlace();
          if (place && onPlaceSelect) {
            onPlaceSelect(place);
          }
        });

        setAutocomplete(autocompleteInstance);
      }
      setIsLoading(false);
    };

    // Initialize autocomplete after a short delay to ensure Google Maps API is loaded
    const timer = setTimeout(initAutocomplete, 1000);
    return () => clearTimeout(timer);
  }, [onPlaceSelect, t, autocomplete]);

  return (
    <div className="relative w-full max-w-2xl mx-auto">
      <div className="flex items-center space-x-2">
        <div className="relative flex-1">
          <Input
            id="location-search"
            type="text"
            placeholder={t('search.placeholder')}
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            className="w-full h-12 pl-12 bg-white text-gray-900"
          />
          <Search className="absolute left-4 top-3 h-6 w-6 text-gray-400" />
        </div>
        <Button 
          className="h-12 px-8 bg-blue-700 hover:bg-blue-800 text-white"
        >
          {isLoading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            t('search.button')
          )}
        </Button>
      </div>
    </div>
  );
}
