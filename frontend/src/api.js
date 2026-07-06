const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

export async function searchFlights(origin, destination, date) {
  const params = new URLSearchParams({ origin, destination, date });
  let response;
  try {
    response = await fetch(`${API_BASE}/search?${params.toString()}`);
  } catch (networkErr) {
    throw new ApiError('Could not reach the backend. Is it running?', 0);
  }

  let body = null;
  try {
    body = await response.json();
  } catch {
    // no body / not JSON
  }

  if (!response.ok) {
    const message = body?.detail || body?.error || `Search failed (${response.status})`;
    throw new ApiError(typeof message === 'string' ? message : JSON.stringify(message), response.status);
  }

  return body;
}
