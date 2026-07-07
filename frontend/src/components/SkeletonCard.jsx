import React from 'react';

// Placeholder shown while a search is in flight. Mirrors the rough shape of
// a FlightCard so the layout doesn't jump when real results arrive.
export default function SkeletonCard() {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 animate-pulse">
      <div className="flex items-center justify-between mb-6">
        <div className="h-5 w-20 bg-slate-200 rounded-full" />
        <div className="h-6 w-24 bg-slate-200 rounded" />
      </div>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="h-4 w-24 bg-slate-200 rounded" />
          <div className="h-px flex-1 mx-4 bg-slate-100" />
          <div className="h-4 w-24 bg-slate-200 rounded" />
        </div>
        <div className="h-8 w-40 bg-slate-100 rounded-lg" />
        <div className="flex items-center justify-between">
          <div className="h-4 w-24 bg-slate-200 rounded" />
          <div className="h-px flex-1 mx-4 bg-slate-100" />
          <div className="h-4 w-24 bg-slate-200 rounded" />
        </div>
      </div>
      <div className="mt-6 pt-4 border-t border-slate-100 flex justify-between">
        <div className="h-4 w-32 bg-slate-200 rounded" />
        <div className="h-4 w-20 bg-slate-200 rounded" />
      </div>
    </div>
  );
}
