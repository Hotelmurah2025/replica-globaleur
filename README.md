# Cemelin Travel - Travel Destination Platform

A modern travel destination platform built with React and FastAPI, featuring interactive maps, trip planning, and multi-language support.

## Live Demo

- Frontend: [https://travel-destination-app-75inxnsu.devinapps.com](https://travel-destination-app-75inxnsu.devinapps.com)
- Backend API: [https://app-okbupxoh.fly.dev/api/v1](https://app-okbupxoh.fly.dev/api/v1)

## Project Structure
- `/frontend` - React.js frontend application with TypeScript and TailwindCSS
- `/cemelin-backend` - FastAPI backend application with PostgreSQL database

## Technologies Used

### Frontend
- React.js with TypeScript
- Vite for build tooling
- TailwindCSS for styling
- React Router for navigation
- i18next for internationalization
- Google Maps API for location services

### Backend
- FastAPI (Python)
- PostgreSQL database
- SQLAlchemy ORM
- Pydantic for data validation
- JWT for authentication
- Google Maps API for geocoding

### Deployment
- Frontend: Vercel
- Backend: Fly.dev
- Database: PostgreSQL (managed by Fly.dev)

## Features

1. **Location Search**
   - Autocomplete for popular locations
   - Google Maps integration
   - Interactive map markers

2. **Destination Details**
   - Detailed information about destinations
   - Photo galleries
   - Location information

3. **Trip Planning**
   - Create and manage travel plans
   - Drag-and-drop interface
   - Day-by-day itinerary planning

4. **User Authentication**
   - User registration
   - Login functionality
   - Secure session management

5. **Reviews System**
   - View and submit reviews
   - Rating system
   - User feedback

6. **Contact Form**
   - Input validation
   - Form submission handling

7. **Multi-language Support**
   - English
   - Indonesian

## Development Setup

### Prerequisites
- Node.js (v18 or higher)
- Python (3.12 or higher)
- PostgreSQL
- pnpm package manager
- Google Maps API key

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Create `.env` file:
   ```
   VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   VITE_API_URL=http://localhost:8000/api/v1
   ```

4. Start development server:
   ```bash
   pnpm dev
   ```

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd cemelin-backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Create `.env` file:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/cemelin
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   JWT_SECRET=your_jwt_secret
   ```

5. Start development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

The API documentation is available at `/docs` when running the backend server:
- Production: [https://app-okbupxoh.fly.dev/docs](https://app-okbupxoh.fly.dev/docs)
- Development: [http://localhost:8000/docs](http://localhost:8000/docs)

## Environment Variables

### Frontend (.env)
- `VITE_GOOGLE_MAPS_API_KEY`: Google Maps API key
- `VITE_API_URL`: Backend API URL

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `GOOGLE_MAPS_API_KEY`: Google Maps API key
- `JWT_SECRET`: Secret key for JWT token generation
- `CORS_ORIGINS`: Allowed CORS origins

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License.
