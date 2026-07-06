import React from 'react';
import { ArrowRight, Clock, Banknote } from 'lucide-react';

// Backend times are local-to-the-airport ISO strings (e.g. "2024-03-15T08:30:00").
// We format them as wall-clock time without any timezone conversion.
function formatTime(isoLocal) {
  const [datePart, timePart] = isoLocal.split('T');
  const [hh, mm] = timePart.split(':');
  const hour = parseInt(hh, 10);
  const period = hour >= 12 ? 'PM' : 'AM';
  const displayHour = hour % 12 === 0 ? 12 : hour % 12;
  return { time: `${displayHour}:${mm} ${period}`, date: datePart };
}

function formatDuration(totalMinutes) {
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return `${hours}h ${minutes}m`;
}

export default function FlightCard({ itinerary }) {
  const { segments, layovers = [], totalDurationMinutes, totalPrice } = itinerary;

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden border border-slate-200">
      <div className="p-6">
        <div className="flex flex-col gap-4">
          {segments.map((segment, idx) => {
            const dep = formatTime(segment.departureTime);
            const arr = formatTime(segment.arrivalTime);
            return (
              <React.Fragment key={segment.flightNumber + idx}>
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <div className="flex flex-col">
                    <span className="text-lg font-extrabold text-slate-900">{segment.flightNumber}</span>
                    <span className="text-xs text-slate-500 uppercase tracking-wide">{segment.airline}</span>
                  </div>

                  <div className="flex items-center gap-3 text-sm font-medium text-slate-700">
                    <div className="text-right">
                      <div className="font-semibold">{dep.time}</div>
                      <div className="text-xs text-slate-500">{segment.origin}</div>
                    </div>
                    <ArrowRight className="text-blue-500" size={16} />
                    <div>
                      <div className="font-semibold">{arr.time}</div>
                      <div className="text-xs text-slate-500">{segment.destination}</div>
                    </div>
                  </div>

                  <div className="text-right text-sm font-semibold text-slate-700">
                    ${segment.price.toFixed(2)}
                  </div>
                </div>

                {idx < segments.length - 1 && layovers[idx] && (
                  <div className="flex items-center gap-2 text-orange-600 bg-orange-50 px-3 py-2 rounded-lg text-sm">
                    <Clock size={14} />
                    <span>
                      Layover in {layovers[idx].airport}: {formatDuration(layovers[idx].durationMinutes)}
                    </span>
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>

        <div className="mt-6 pt-4 border-t border-slate-100 flex justify-between items-center flex-wrap gap-2">
          <div className="flex items-center gap-2 text-slate-600 font-medium text-sm">
            <Clock size={16} />
            <span>Total duration: {formatDuration(totalDurationMinutes)}</span>
          </div>
          <div className="flex items-center gap-2 text-blue-700 font-bold text-lg">
            <Banknote size={20} />
            <span>${totalPrice.toFixed(2)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
