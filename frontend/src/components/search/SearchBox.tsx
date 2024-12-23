import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Search, Loader2 } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { toast } from '@/components/ui/use-toast';

interface Location {
  place_id: string;
  name: string;
  description: string;
  location: {
    lat: number;
    lng: number;
  };
}

interface SearchBoxProps {
  onPlaceSelect?: (place: Location) => void;
}

export function SearchBox({ onPlaceSelect }: SearchBoxProps) {
  const { t } = useTranslation();
  const [searchInput, setSearchInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<Location[]>([]);

  useEffect(() => {
    const searchLocations = async () => {
      if (!searchInput.trim()) {
        setSuggestions([]);
        return;
      }

      setIsLoading(true);
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/locations/search?` + 
          new URLSearchParams({ 
            query: searchInput,
            language: t('common.languageCode')
          })
        );
        
        if (!response.ok) {
          throw new Error('Search failed');
        }

        const data = await response.json();
        setSuggestions(data);
      } catch (error) {
        console.error('Search error:', error);
        toast({
          title: t('search.error'),
          description: t('search.searchError'),
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };

    const debounceTimer = setTimeout(searchLocations, 300);
    return () => clearTimeout(debounceTimer);
  }, [searchInput, t]);

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
          {suggestions.length > 0 && (
            <div className="absolute w-full mt-1 bg-white rounded-md shadow-lg z-50">
              <ul className="py-1">
                {suggestions.map((suggestion) => (
                  <li
                    key={suggestion.place_id}
                    className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                    onClick={() => {
                      setSearchInput(suggestion.name);
                      setSuggestions([]);
                      if (onPlaceSelect) {
                        onPlaceSelect(suggestion);
                      }
                    }}
                  >
                    <div className="font-medium">{suggestion.name}</div>
                    <div className="text-sm text-gray-500">{suggestion.description}</div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
        <Button 
          className="h-12 px-8 bg-blue-700 hover:bg-blue-800 text-white"
          disabled={isLoading}
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
