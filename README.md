# SkyPath — Flight Connection Search Engine

A small full-stack app for searching direct and connecting flight itineraries between two airports, with correct timezone-aware layover calculations.

## Structure

```
skypath/
├── backend/           FastAPI service (Python)
│   ├── app/
│   │   ├── data.py        loads flights.json, indexes airports + flights-by-origin
│   │   ├── timezones.py   logic for time processing
│   │   ├── search.py      DFS itinerary search + flight validation
│   │   ├── itinerary.py   turns a flight path into the API response shap
│   │   ├── schemas.py     Pydantic response models, frontend API contract
│   │   └── main.py        route handlers: input validation + wiring
│   └── tests/          pytest suite, one file per module
├── frontend/           React + Vite + Tailwind SPA
│   └── src/
│       ├── api.js               fetch wrapper, raises ApiError on non-2xx
│       ├── App.jsx               page state: loading / error / empty / results
│       └── components/           SearchForm, FlightCard, SkeletonCard
├── flights.json         the dataset (25 airports, ~260 flights)
└── docker-compose.yml
```

## How to run

**Docker (recommended):**

```bash
docker-compose up
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

**Running tests:**

```bash
cd backend
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

## Assumptions Made

- The 6hr max layover is per flight not per itinerary.
- Domestic connection. It is defined as "if both arriving and departing flights are within the same country". So if we have an edge case such as JFK->CDG->LAX (via Paris) the code will still think this is domestic since JFK and LAX are within the same country.
- If bad data is read, the app skips instead of crash.
- No revisiting any airport in path.
- 45m/90m layover minimum is uniform accross all airports.
- Total duration is the first departure till last arrival including layover time.
- Price are assumed in dollars ($).
- Reject if origin and destination is the same.

## Architecture decisions



## Tradeoffs considered



## What I'd improve with more time

- **CI**: run `pytest` and a frontend lint/build check on every push; currently tests only run manually.
- **Stricter data validation at load time**: log (or flag using `/health`) how many records were skipped and why, instead of silently dropping malformed ones.
- **Pagination / result limits**: `find_itineraries` returns every valid path. On a much larger dataset this could grow large enough to want a limit or streaming response.
- **Frontend**: sort/filter controls (by price, by stops), airline logos/branding if the dataset ever has more than one airline, component/integration tests (currently untested).
- **Observability**: structured (JSON) logging and request IDs instead of the current plain-text logger, so logs are queryable in a real deployment. Add tracing, record request latency, for when things get larger.
- **Auth/rate limiting**: the API is fully open right now, not ready for public use.
