"""
Pydantic response models. Used by frotnend
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
    layovers: list[Layover]
    totalDurationMinutes: int
    totalPrice: float


class SearchResponse(BaseModel):
    origin: str
    destination: str
    itineraries: list[Itinerary]
