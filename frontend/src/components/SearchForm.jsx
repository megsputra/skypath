import React, { useState } from 'react';
import { Search } from 'lucide-react';

const IATA_RE = /^[A-Z]{3}$/;

function validate({ origin, destination, date }) {
  const errors = {};
  if (!origin || !IATA_RE.test(origin)) {
    errors.origin = 'Enter a valid 3-letter IATA code (e.g. JFK)';
  }
  if (!destination || !IATA_RE.test(destination)) {
    errors.destination = 'Enter a valid 3-letter IATA code (e.g. LAX)';
  }
  if (!errors.origin && !errors.destination && origin === destination) {
    errors.destination = 'Destination must differ from origin';
  }
  if (!date) {
    errors.date = 'Select a travel date';
  }
  return errors;
}

export default function SearchForm({ onSearch, disabled }) {
  const [formData, setFormData] = useState({ origin: '', destination: '', date: '' });
  const [errors, setErrors] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validate(formData);
    setErrors(validationErrors);
    if (Object.keys(validationErrors).length === 0) {
      onSearch(formData);
    }
  };

  const updateField = (field) => (e) => {
    const value = field === 'date' ? e.target.value : e.target.value.toUpperCase();
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <div className="bg-white rounded-xl shadow-xl p-6">
      <form onSubmit={handleSubmit} noValidate className="grid grid-cols-1 md:grid-cols-4 gap-4 items-start">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1" htmlFor="origin">
            Origin (IATA)
          </label>
          <input
            id="origin"
            type="text"
            placeholder="e.g. JFK"
            className={`w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 uppercase ${
              errors.origin ? 'border-red-400' : 'border-slate-300'
            }`}
            value={formData.origin}
            onChange={updateField('origin')}
            maxLength={3}
          />
          {errors.origin && <p className="text-xs text-red-600 mt-1">{errors.origin}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1" htmlFor="destination">
            Destination (IATA)
          </label>
          <input
            id="destination"
            type="text"
            placeholder="e.g. LAX"
            className={`w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 uppercase ${
              errors.destination ? 'border-red-400' : 'border-slate-300'
            }`}
            value={formData.destination}
            onChange={updateField('destination')}
            maxLength={3}
          />
          {errors.destination && <p className="text-xs text-red-600 mt-1">{errors.destination}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1" htmlFor="date">
            Date
          </label>
          <input
            id="date"
            type="date"
            className={`w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 ${
              errors.date ? 'border-red-400' : 'border-slate-300'
            }`}
            value={formData.date}
            onChange={updateField('date')}
          />
          {errors.date && <p className="text-xs text-red-600 mt-1">{errors.date}</p>}
        </div>

        <button
          type="submit"
          disabled={disabled}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed text-white font-bold py-2 px-4 rounded flex items-center justify-center gap-2 transition-colors h-[42px]"
        >
          <Search size={18} />
          {disabled ? 'Searching…' : 'Search Flights'}
        </button>
      </form>
    </div>
  );
}
