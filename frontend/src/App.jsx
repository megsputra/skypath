import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import FlightCard from './components/FlightCard';
import SkeletonCard from './components/SkeletonCard';
import { Plane, AlertCircle, SearchX } from 'lucide-react';
import { searchFlights } from './api';

// Results arrive sorted by duration (backend), so index 0 is always fastest.
// Cheapest can be any index, so we find it here to tag the right card.
function cheapestIndex(itineraries) {
  if (itineraries.length === 0) return -1;
  let best = 0;
  itineraries.forEach((it, i) => {
    if (it.totalPrice < itineraries[best].totalPrice) best = i;
  });
  return best;
}

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

  const cheapest = itineraries ? cheapestIndex(itineraries) : -1;

  return (
    <div className="min-h-screen bg-slate-50 pb-20">
      <header className="bg-gradient-to-r from-indigo-600 to-blue-600 text-white py-10 shadow-lg">
        <div className="container mx-auto px-4 flex items-center gap-3">
          <div className="bg-white/15 rounded-xl p-2">
            <Plane size={26} />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight leading-none">SkyPath</h1>
            <p className="text-sm text-indigo-100 mt-1">Flight connection search</p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 -mt-8">
        <SearchForm onSearch={handleSearch} disabled={loading} />

        {loading && (
          <div className="mt-8 grid gap-5 max-w-4xl mx-auto" role="status" aria-live="polite">
            <span className="sr-only">Searching for flights…</span>
            <SkeletonCard />
            <SkeletonCard />
            <SkeletonCard />
          </div>
        )}

        {!loading && error && (
          <div className="mt-8 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 flex items-center gap-3 rounded-lg max-w-4xl mx-auto">
            <AlertCircle size={20} className="shrink-0" />
            <p>{error}</p>
          </div>
        )}

        {!loading && !error && itineraries !== null && (
          <div className="mt-8 max-w-4xl mx-auto">
            {itineraries.length > 0 ? (
              <>
                <p className="text-sm text-slate-500 mb-4 px-1">
                  {itineraries.length} {itineraries.length === 1 ? 'itinerary' : 'itineraries'} found · sorted by
                  travel time
                </p>
                <div className="grid gap-5">
                  {itineraries.map((itinerary, idx) => (
                    <FlightCard
                      key={idx}
                      itinerary={itinerary}
                      isFastest={itineraries.length > 1 && idx === 0}
                      isCheapest={itineraries.length > 1 && idx === cheapest}
                    />
                  ))}
                </div>
              </>
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
