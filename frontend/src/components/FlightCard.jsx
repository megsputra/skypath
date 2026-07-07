import React from 'react';
import { Plane, Clock, Zap, Tag } from 'lucide-react';

// Backend times are local-to-the-airport ISO strings (e.g. "2024-03-15T08:30:00").
// We format them as wall-clock time without any timezone conversion.
function formatTime(isoLocal) {
  const [, timePart] = isoLocal.split('T');
  const [hh, mm] = timePart.split(':');
  const hour = parseInt(hh, 10);
  const period = hour >= 12 ? 'PM' : 'AM';
  const displayHour = hour % 12 === 0 ? 12 : hour % 12;
  return `${displayHour}:${mm} ${period}`;
}

function formatDuration(totalMinutes) {
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return `${hours}h ${minutes}m`;
}

function stopLabel(segmentCount) {
  const stops = segmentCount - 1;
  if (stops === 0) return 'Direct';
  return stops === 1 ? '1 stop' : `${stops} stops`;
}

export default function FlightCard({ itinerary, isFastest, isCheapest }) {
  const { segments, layovers = [], totalDurationMinutes, totalPrice } = itinerary;
  const stops = segments.length - 1;

  return (
    <div className="group bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-200">
      <div className="p-6">
        {/* Header: stop count + tags on the left, total price on the right */}
        <div className="flex items-start justify-between gap-3 mb-5">
          <div className="flex flex-wrap items-center gap-2">
            <span
              className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                stops === 0 ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'
              }`}
            >
              {stopLabel(segments.length)}
            </span>
            {isFastest && (
              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-700">
                <Zap size={12} /> Fastest
              </span>
            )}
            {isCheapest && (
              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700">
                <Tag size={12} /> Cheapest
              </span>
            )}
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-slate-900 leading-none">${totalPrice.toFixed(2)}</div>
            <div className="text-xs text-slate-400 mt-1">total</div>
          </div>
        </div>

        {/* Segment timeline */}
        <div className="space-y-3">
          {segments.map((segment, idx) => (
            <React.Fragment key={segment.flightNumber + idx}>
              <div className="flex items-center gap-4">
                {/* Departure */}
                <div className="w-20 shrink-0">
                  <div className="text-base font-semibold text-slate-900">{formatTime(segment.departureTime)}</div>
                  <div className="text-xs font-medium text-slate-400">{segment.origin}</div>
                </div>

                {/* Connector with flight info */}
                <div className="flex-1 flex flex-col items-center">
                  <div className="text-xs font-medium text-slate-500">
                    {segment.flightNumber} · {segment.airline}
                  </div>
                  <div className="w-full flex items-center gap-1 my-1">
                    <div className="h-px flex-1 bg-slate-200" />
                    <Plane size={14} className="text-indigo-500 rotate-90" />
                    <div className="h-px flex-1 bg-slate-200" />
                  </div>
                </div>

                {/* Arrival */}
                <div className="w-20 shrink-0 text-right">
                  <div className="text-base font-semibold text-slate-900">{formatTime(segment.arrivalTime)}</div>
                  <div className="text-xs font-medium text-slate-400">{segment.destination}</div>
                </div>
              </div>

              {idx < segments.length - 1 && layovers[idx] && (
                <div className="flex items-center gap-2 text-amber-700 bg-amber-50/70 px-3 py-1.5 rounded-lg text-xs font-medium w-fit mx-auto">
                  <Clock size={12} />
                  <span>
                    {formatDuration(layovers[idx].durationMinutes)} layover in {layovers[idx].airport}
                  </span>
                </div>
              )}
            </React.Fragment>
          ))}
        </div>

        {/* Footer: total duration */}
        <div className="mt-5 pt-4 border-t border-slate-100 flex items-center gap-2 text-slate-500 text-sm">
          <Clock size={15} />
          <span className="font-medium">{formatDuration(totalDurationMinutes)} total travel time</span>
        </div>
      </div>
    </div>
  );
}
