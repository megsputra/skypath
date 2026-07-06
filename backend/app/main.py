"""
SkyPath backend - Flight Connection Search Engine

Route handlers only: validate input, then delegate to data/search/itinerary
modules. Keep it thin -- if a handler needs more than a few lines of logic,
that logic belongs in one of the other modules instead.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .data import load_flight_data
from .itinerary import build_and_sort_itineraries
from .schemas import SearchResponse
from .search import find_itineraries

app = FastAPI(title="SkyPath API")

# Allow the frontend (served separately) to call this API during local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loaded once at startup. NB: this will raise NotImplementedError until
# data.load_flight_data() is implemented (step 1/3) -- that's expected,
# implement that module first.
flight_data = load_flight_data()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search", response_model=SearchResponse)
def search(
    origin: str = Query(..., description="Origin airport code, e.g. SFO"),
    destination: str = Query(..., description="Destination airport code, e.g. JFK"),
    date: str = Query(..., description="Travel date, YYYY-MM-DD"),
):
    origin = origin.upper()
    destination = destination.upper()

    # Step 2 (merged into main.py) -- TODO:
    # - origin/destination must exist in flight_data.airports -> else 404
    #   "Unknown airport code: XXX"
    # - origin == destination -> 400
    # - date must parse as YYYY-MM-DD (see datetime.date.fromisoformat) -> else 400

    paths = find_itineraries(flight_data, origin, destination, date)
    itineraries = build_and_sort_itineraries(flight_data, paths)

    return SearchResponse(
        origin=origin, destination=destination, itineraries=itineraries
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
