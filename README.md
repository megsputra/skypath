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
docker-compose up frontend # will bring up backend
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

**Running tests:**

```bash
cd backend
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

## Assumptions made

- The 6hr max layover is per flight, not per itinerary. So a 2-stop itinerary with >6hr layovers is considered valid.
- Domestic connection. It is defined as "if both arriving and departing flights are within the same country". So if we have an edge case such as JFK->CDG->LAX (via Paris) the code will still think this is domestic since JFK and LAX are within the same country.
- If bad data is read, the app skips instead of crashing.
- No airport changes at a layover, only looking at flights departing from the airport we landed at.
- No revisiting an airport already in the path. Example: if traveling JFK -> LAX, JFK -> ORD -> JFK -> LAX is invalid.
- 45m/90m layover minimum is uniform across all airports.
- Total duration is the first departure till last arrival, including layover time.
- Prices are assumed in dollars ($).
- Reject if origin and destination are the same.

## Architecture decisions

- Split backend into single purpose modules for isolation and organization.
- All timezone calculations goes through `to_utc()` and won't use raw string comparison.
- Flight map, keyed by origin (airport code), containing all destinations from that origin are stored as a dict, enabling O(1) lookups of "where can I fly from here". This avoids scanning the whole flight catalog.
- Use DFS as the main search algorithm, capped at 3 recursive steps. Keeps a set of visited nodes so won't revisit the same airport (see assumptions above and tradeoffs below)
- Use Pydantic schema as API contract. The frontend is built upon these field names.
- Added a global HTTPException handler for logging rather than logging.warning() for any rejected request, use FastAPI's default response. Keeps validation checks one line while still showing the "why" in Docker logs
- Plain fetch on the frontend side, without data fetching libraries. This could be improved with a library like React Query, but not used given the load of this app.

## Tradeoffs considered

- DFS vs shortest path algorithms. Algorithms like Dijkstra would scale better on a larger dataset, but would need reworking to enumerate all valid itineraries. At ~260 flights, DFS is fast and easy to reason about; I’d revisit this if the dataset were, say, 100x larger.
- Skipping bad data vs failing. Some flights have a price as a string instead of a number. Instead of crashing and failing the total price count at the end, our logic skips it. The tradeoff is that a bad record disappears silently. Acceptable for a few known data variants in this use case, but I’d add a startup-time warning log (or a stricter fail-fast mode) before trusting this against real data.
- Open CORS allow_origins=[“*”]. Fine for this purpose, where frontend and backend run on different ports, but wrong for production. This would need to be pinned to the actual frontend origin.
- No database. The dataset loads once into in-memory dicts at startup. Simpler and fast enough for this purpose, but means no persistence, no updates without a restart, and the whole dataset must fit in memory.


## What I'd improve with more time

- **CI**: run `pytest` and a frontend lint/build check on every push; currently tests only run manually.
- **Stricter data validation at load time**: log (or flag using `/health`) how many records were skipped and why, instead of silently dropping malformed ones.
- **Pagination / result limits**: `find_itineraries` returns every valid path. On a much larger dataset this could grow large enough to want a limit or streaming response.
- **Frontend**: sort/filter controls (by price, by stops), airline logos/branding if the dataset ever has more than one airline, component/integration tests (currently untested).
- **Observability**: structured (JSON) logging and request IDs instead of the current plain-text logger, so logs are queryable in a real deployment. Add tracing, record request latency, for when things get larger.
- **Auth/rate limiting**: the API is fully open right now, not ready for public use.
