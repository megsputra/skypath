import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import FlightCard from './components/FlightCard';
import { Plane, AlertCircle, Loader2, SearchX } from 'lucide-react';
import { searchFlights } from './api';

function App() {
  const [itineraries, setItineraries] = useState(null); // null = no search yet
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async ({ origin, destination, date }) => {
    setLoading(true);
    setError(null);
    setItineraries(null);
    try {
      const data = await searchFlights(origin, destination, date);
      setItineraries(data.itineraries ?? []);
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-20">
      <header className="bg-blue-600 text-white py-8 shadow-lg">
        <div className="container mx-auto px-4 flex items-center gap-3">
          <Plane size={32} />
          <h1 className="text-3xl font-bold tracking-tight">SkyPath</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 -mt-8">
        <SearchForm onSearch={handleSearch} disabled={loading} />

        {loading && (
          <div className="flex justify-center my-12 text-blue-600" role="status" aria-live="polite">
            <Loader2 className="animate-spin" size={48} />
          </div>
        )}

        {!loading && error && (
          <div className="mt-8 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 flex items-center gap-3 rounded">
            <AlertCircle size={20} className="shrink-0" />
            <p>{error}</p>
          </div>
        )}

        {!loading && !error && itineraries !== null && (
          <div className="mt-8 grid gap-6 max-w-4xl mx-auto">
            {itineraries.length > 0 ? (
              itineraries.map((itinerary, idx) => <FlightCard key={idx} itinerary={itinerary} />)
            ) : (
              <div className="text-center py-16 text-slate-500 flex flex-col items-center gap-3">
                <SearchX size={40} className="text-slate-400" />
                <p className="text-xl font-medium">No flights found for this route.</p>
                <p className="text-sm">Try a different date or airport pair.</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
