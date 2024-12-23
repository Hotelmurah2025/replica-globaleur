import { useState } from "react"
import { useLoadScript } from "@react-google-maps/api"
import { MapView } from "../components/maps/MapView"
import { SearchBox } from "../components/search/SearchBox"
import { Button } from "../components/ui/button"
import { Helmet } from "react-helmet-async"
import { useTranslation } from "react-i18next"

const libraries: ("places")[] = ["places"]

interface Destination {
  id: string
  name: string
  description: string
  image: string
  location: {
    lat: number
    lng: number
  }
  activities: string[]
}

const mockDestinations: Destination[] = [
  {
    id: "1",
    name: "Bali",
    description: "Experience the magic of Bali with its pristine beaches, lush landscapes, and vibrant cultural heritage. From ancient temples to modern beach clubs, Bali offers something for every traveler.",
    image: "https://source.unsplash.com/800x600/?bali,beach",
    location: {
      lat: -8.409518,
      lng: 115.188919,
    },
    activities: [
      "Visit Tanah Lot Temple",
      "Surf at Kuta Beach",
      "Explore Ubud Rice Terraces",
      "Traditional Dance Performance",
      "Sunset at Uluwatu Temple"
    ]
  },
  {
    id: "2",
    name: "Jakarta",
    description: "Discover Jakarta, Indonesia's dynamic capital, where modern skyscrapers meet historical landmarks. Experience the city's rich cultural diversity, shopping districts, and culinary delights.",
    image: "https://source.unsplash.com/800x600/?jakarta,city",
    location: {
      lat: -6.200000,
      lng: 106.816666,
    },
    activities: [
      "Visit National Monument (MONAS)",
      "Shop at Grand Indonesia",
      "Explore Old Town (Kota Tua)",
      "Visit Istiqlal Mosque",
      "Food Tour in Glodok"
    ]
  },
]

export default function Destinations() {
  const { t } = useTranslation();
  const [selectedDestination, setSelectedDestination] = useState<Destination | null>(null)
  const [mapCenter, setMapCenter] = useState({
    lat: -6.200000,
    lng: 106.816666,
  })

  const { isLoaded } = useLoadScript({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || "",
    libraries,
  })

  const handlePlaceSelect = (place: google.maps.places.PlaceResult) => {
    if (place.geometry?.location) {
      setMapCenter({
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng(),
      })
    }
  }

  if (!isLoaded) return <div>{t('common.loading')}</div>

  return (
    <>
      <Helmet>
        <title>{t('destinations.pageTitle')} | Cemelin Travel</title>
        <meta name="description" content={t('destinations.metaDescription')} />
        <meta property="og:title" content={`${t('destinations.pageTitle')} | Cemelin Travel`} />
        <meta property="og:description" content={t('destinations.metaDescription')} />
        <meta property="og:type" content="website" />
      </Helmet>

      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-4">{t('destinations.explore')}</h1>
          <SearchBox onPlaceSelect={handlePlaceSelect} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Destinations List */}
          <div className="lg:col-span-1 space-y-6">
            {mockDestinations.map((destination) => (
              <div
                key={destination.id}
                className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
              >
                <img
                  src={destination.image}
                  alt={destination.name}
                  className="w-full h-48 object-cover"
                />
                <div className="p-4">
                  <h3 className="text-xl font-semibold mb-2">{destination.name}</h3>
                  <p className="text-gray-600 mb-4 line-clamp-3">{destination.description}</p>
                  <Button
                    onClick={() => {
                      setSelectedDestination(destination)
                      setMapCenter(destination.location)
                    }}
                    className="w-full"
                  >
                    {t('destinations.viewDetails')}
                  </Button>
                </div>
              </div>
            ))}
          </div>

          {/* Map and Details View */}
          <div className="lg:col-span-2">
            <div className="sticky top-24 space-y-6">
              <MapView
                center={mapCenter}
                markers={selectedDestination ? [selectedDestination.location] : mockDestinations.map(d => d.location)}
              />
              
              {selectedDestination && (
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h2 className="text-2xl font-bold mb-4">{selectedDestination.name}</h2>
                  <p className="text-gray-600 mb-6">{selectedDestination.description}</p>
                  
                  <h3 className="text-xl font-semibold mb-3">{t('destinations.activities')}</h3>
                  <ul className="space-y-2">
                    {selectedDestination.activities.map((activity, index) => (
                      <li key={index} className="flex items-center text-gray-700">
                        <span className="mr-2">•</span>
                        {activity}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
