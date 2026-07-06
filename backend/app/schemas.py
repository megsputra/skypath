"""
Pydantic response models -- this is the API contract the frontend was
built against (see frontend/src/api.js and frontend/src/components/FlightCard.jsx).
Don't change field names/shapes here without updating the frontend too.
"""

from pydantic import BaseModel


class Segment(BaseModel):
    flightNumber: str
    airline: str
    origin: str
    destination: str
    departureTime: str
    arrivalTime: str
    price: float


class Layover(BaseModel):
    airport: str
    durationMinutes: int


class Itinerary(BaseModel):
    segments: list[Segment]
    layovers: list[Layover]  # length == len(segments) - 1
    totalDurationMinutes: int
    totalPrice: float


class SearchResponse(BaseModel):
    origin: str
    destination: str
    itineraries: list[Itinerary]
