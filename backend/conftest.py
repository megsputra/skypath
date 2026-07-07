import os

os.environ.setdefault(
    "FLIGHTS_JSON_PATH",
    os.path.join(os.path.dirname(__file__), "..", "flights.json"),
)
