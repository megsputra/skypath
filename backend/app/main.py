"""
SkyPath backend - Flight Connection Search Engine

Route handlers only: validate input, then delegate to data/search/itinerary
modules. Keep it thin -- if a handler needs more than a few lines of logic,
that logic belongs in one of the other modules instead.
"""

import logging
from datetime import date as date_cls

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

from .data import load_flight_data
from .itinerary import build_and_sort_itineraries
from .schemas import SearchResponse
from .search import find_itineraries

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("skypath")

app = FastAPI(title="SkyPath API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

flight_data = load_flight_data()


@app.exception_handler(HTTPException)
async def log_http_exceptions(request: Request, exc: HTTPException):
    # Log reason when encountering HTTP exception
    query = f"?{request.url.query}" if request.url.query else ""
    logger.warning(
        "%s %s%s -> %s %s",
        request.method,
        request.url.path,
        query,
        exc.status_code,
        exc.detail,
    )
    return await http_exception_handler(request, exc)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search", response_model=SearchResponse)
def search(
    origin: str = Query(..., description="Origin airport code, e.g. SFO"),
    destination: str = Query(..., description="Destination airport code, e.g. JFK"),
    date: str = Query(..., description="Travel date, YYYY-MM-DD"),
):
    origin = origin.strip().upper()
    destination = destination.strip().upper()

    if origin not in flight_data.airports:
        raise HTTPException(status_code=404, detail=f"Unknown airport code: {origin}")
    if destination not in flight_data.airports:
        raise HTTPException(
            status_code=404, detail=f"Unknown airport code: {destination}"
        )

    if origin == destination:
        raise HTTPException(
            status_code=400, detail="Origin and destination must not be the same."
        )

    try:
        date = date_cls.fromisoformat(date).isoformat()
    except ValueError:
        raise HTTPException(status_code=400, detail="date must be in YYYY-MM-DD format")

    paths = find_itineraries(flight_data, origin, destination, date)
    itineraries = build_and_sort_itineraries(flight_data, paths)

    return SearchResponse(
        origin=origin, destination=destination, itineraries=itineraries
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
