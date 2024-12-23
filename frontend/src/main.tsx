import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import './i18n'

// Load Google Maps API
const googleMapsScript = document.createElement('script')
googleMapsScript.src = `https://maps.googleapis.com/maps/api/js?key=${import.meta.env.VITE_GOOGLE_MAPS_API_KEY}&libraries=places`
googleMapsScript.async = true
googleMapsScript.defer = true
document.head.appendChild(googleMapsScript)

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
