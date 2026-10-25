"""
app.py - Main Streamlit entry point for the Personalized Travel Itinerary Planner.
Skill Wallet Capstone Project 4.

Run with:
    streamlit run app.py
"""

import streamlit as st

# ── Page Config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Personalized Travel Itinerary Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com",
        "Report a bug": None,
        "About": "Personalized Travel Itinerary Planner — Skill Wallet Capstone Project 4",
    },
)

# ── Internal imports (after set_page_config) ──────────────────────────────────
from frontend.styles import get_css
from backend.config import (
    APP_NAME, APP_TAGLINE, APP_VERSION,
    VIBES, BUDGET_LEVELS, TRAVEL_PARTY, PACE_OPTIONS, INTERESTS,
)
from backend.trip_db import init_db
from backend.ai_client import get_active_api_key
from frontend.tabs.tab1_destinations import render_tab1
from frontend.tabs.tab2_itinerary import render_tab2
from frontend.tabs.tab3_vibe import render_tab3
from frontend.tabs.tab4_management import render_tab4

# ── Inject CSS ────────────────────────────────────────────────────────────────
st.markdown(get_css(), unsafe_allow_html=True)

# ── Initialize DB ─────────────────────────────────────────────────────────────
init_db()

# ── Session Defaults ──────────────────────────────────────────────────────────
def _init_session():
    defaults = {
        "ai_provider": "gemini",
        "api_key": "",
        "prefs": {},
        "itinerary": None,
        "destinations_loaded": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_session()


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Configuration & User Preferences (Epic 3)
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo / brand
    st.markdown(f"""
<div style="text-align:center;padding:1.25rem 0 1.5rem;border-bottom:1px solid #E4DDD4;margin-bottom:0.5rem;">
  <div style="font-size:2rem;margin-bottom:0.4rem;">✈</div>
  <div style="font-family:'Cormorant Garamond',Georgia,serif;font-size:1rem;font-weight:600;
              color:#1C1917;letter-spacing:0.01em;line-height:1.3;">
    {APP_NAME}
  </div>
  <div style="color:#A89F98;font-size:0.68rem;margin-top:0.3rem;letter-spacing:0.1em;text-transform:uppercase;">v{APP_VERSION}</div>
</div>
""", unsafe_allow_html=True)

    # ── API Configuration ─────────────────────────────────────────────────────
    with st.expander("🔑 AI Engine Settings", expanded=False):
        provider = st.selectbox(
            "AI Provider",
            ["gemini", "groq", "demo"],
            format_func=lambda x: {
                "gemini": "🤖 Google Gemini (Default)",
                "groq": "⚡ Groq (LLaMA3)",
                "demo": "⚡ Offline Demo Mode",
            }.get(x, x),
            key="ai_provider",
        )

        if provider != "demo":
            api_key_label = "Gemini API Key" if provider == "gemini" else "Groq API Key"
            active_key = get_active_api_key(provider)
            api_key = st.text_input(
                api_key_label,
                type="password",
                placeholder="Key active from secrets, or paste custom key…",
                key="api_key",
            )
            resolved_key = active_key or api_key
            if resolved_key:
                st.markdown("""<div class="status-pill status-live">✅ Live AI Active</div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="status-pill status-demo">⚠️ No key found — demo fallback</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="status-pill status-demo">⚡ Offline Demo Mode</div>""", unsafe_allow_html=True)
            st.caption("Switch to Google Gemini for real-time live generation.")

    st.markdown("---")

    # ── Trip Preferences Form ─────────────────────────────────────────────────
    st.markdown("<p style='font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:#A89F98;font-weight:500;margin-bottom:0.75rem;'>Trip Preferences</p>", unsafe_allow_html=True)

    destination = st.text_input(
        "📍 Destination (optional)",
        placeholder="e.g. Tokyo, Japan — or leave blank for recommendations",
        key="dest_input",
    )

    vibe = st.selectbox("🎯 Travel Vibe", VIBES, key="vibe_input")

    col_dur, col_dates = st.columns(2)
    with col_dur:
        duration = st.number_input("🌙 Days", min_value=1, max_value=21, value=3, key="duration_input")
    with col_dates:
        travel_dates = st.text_input("🗓 Dates", placeholder="e.g. Dec 15–22", key="dates_input")

    budget = st.selectbox("💰 Budget Level", BUDGET_LEVELS, index=1, key="budget_input")
    party = st.selectbox("👥 Travel Party", TRAVEL_PARTY, key="party_input")
    pace = st.selectbox("🏃 Pace", PACE_OPTIONS, index=1, key="pace_input")

    interests = st.multiselect(
        "🎨 Interests (pick up to 5)",
        INTERESTS,
        default=["Food & Cuisine", "History & Culture"],
        max_selections=5,
        key="interests_input",
    )

    # Compile preferences dict
    prefs = {
        "destination": destination.strip(),
        "vibe": vibe,
        "duration": int(duration),
        "dates": travel_dates,
        "budget": budget,
        "party": party,
        "pace": pace,
        "interests": interests,
    }
    st.session_state["prefs"] = prefs

    st.markdown("---")

    # ── Quick Actions ─────────────────────────────────────────────────────────
    st.markdown("<p style='font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:#A89F98;font-weight:500;margin-bottom:0.5rem;'>Quick Actions</p>", unsafe_allow_html=True)

    if st.button("🔄 Reset Everything", use_container_width=True):
        keys_to_clear = ["itinerary", "destinations", "destinations_loaded", "itin_prefs",
                         "demo_notice", "demo_itin_notice", "selected_destination"]
        for k in keys_to_clear:
            st.session_state.pop(k, None)
        st.success("Session reset!")
        st.rerun()

    # Trip count badge
    from backend.trip_db import get_all_trips
    trip_count = len(get_all_trips())
    if trip_count > 0:
        st.markdown(f"""
<div style="text-align:center;margin-top:0.5rem;">
  <span class="status-pill status-live">🗺️ {trip_count} trip{"s" if trip_count != 1 else ""} saved</span>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT AREA
# ══════════════════════════════════════════════════════════════════════════════

# Hero Header
st.markdown(f"""
<div class="hero-header">
  <div class="hero-title">✈ <em>Travel</em> Planner</div>
  <div class="hero-tagline">{APP_TAGLINE}</div>
  <div class="hero-badges">
    <span class="hero-badge">AI-Powered</span>
    <span class="hero-badge">Geo-Clustered</span>
    <span class="hero-badge">Budget Tracker</span>
    <span class="hero-badge">PDF Export</span>
    <span class="hero-badge">Live Swaps</span>
    <span class="hero-badge">Trip History</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Active trip context strip
active_dest = prefs.get("destination") or st.session_state.get("selected_destination") or "Open to Recommendations"
st.markdown(f"""
<div class="active-trip-strip">
  <span style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;
               color:#8C8276;font-weight:600;margin-right:0.5rem;">Active Trip</span>
  <span class="hero-badge">📍 {active_dest}</span>
  <span class="hero-badge">{prefs['duration']} days</span>
  <span class="hero-badge">{prefs['party']}</span>
  <span class="hero-badge">{prefs['budget']}</span>
</div>
""", unsafe_allow_html=True)

# ── Four Main Tabs ────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Destination Finder",
    "Itinerary Generator",
    "Vibe & Swaps",
    "Trip Management",
])

with tab1:
    render_tab1(prefs)

with tab2:
    # Merge any selected destination into prefs
    active_prefs = dict(prefs)
    if not active_prefs.get("destination") and st.session_state.get("selected_destination"):
        active_prefs["destination"] = st.session_state["selected_destination"]
    render_tab2(active_prefs)

with tab3:
    render_tab3(prefs)

with tab4:
    render_tab4(prefs)
