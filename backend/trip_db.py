"""
trip_db.py - Simulated in-memory / JSON-file trip database.
Zero external database dependencies. Uses Streamlit session state +
an optional local JSON file for persistence across reloads.
"""

from __future__ import annotations
import json
import os
import uuid
from datetime import datetime
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "trip_history.json")


def _load_db() -> list[dict]:
    """Load trip history from local JSON file."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _save_db(trips: list[dict]) -> None:
    """Persist trip history to local JSON file."""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(trips, f, ensure_ascii=False, indent=2)
    except IOError:
        pass  # Graceful degradation on read-only filesystems (e.g. Streamlit Cloud)


def init_db() -> None:
    """Initialize the trip history in session state."""
    if "trip_history" not in st.session_state:
        st.session_state.trip_history = _load_db()


def save_trip(itinerary: dict, prefs: dict) -> str:
    """Save a trip to the database. Returns the trip ID."""
    init_db()
    trip_id = str(uuid.uuid4())[:8].upper()
    trip_record = {
        "id": trip_id,
        "destination": itinerary.get("destination", "Unknown"),
        "duration": itinerary.get("duration", 0),
        "budget": prefs.get("budget", "Moderate"),
        "party": prefs.get("party", "Solo"),
        "dates": prefs.get("dates", ""),
        "total_cost_usd": itinerary.get("total_cost_usd", 0),
        "total_cost_inr": itinerary.get("total_cost_inr", 0),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "itinerary": itinerary,
        "prefs": prefs,
    }
    st.session_state.trip_history.insert(0, trip_record)
    _save_db(st.session_state.trip_history)
    return trip_id


def get_all_trips() -> list[dict]:
    """Return all saved trips (newest first)."""
    init_db()
    return st.session_state.trip_history


def get_trip(trip_id: str) -> dict | None:
    """Return a single trip by ID."""
    init_db()
    for trip in st.session_state.trip_history:
        if trip["id"] == trip_id:
            return trip
    return None


def delete_trip(trip_id: str) -> None:
    """Remove a trip from the database."""
    init_db()
    st.session_state.trip_history = [
        t for t in st.session_state.trip_history if t["id"] != trip_id
    ]
    _save_db(st.session_state.trip_history)


def clear_all_trips() -> None:
    """Wipe all trip history."""
    st.session_state.trip_history = []
    _save_db([])
