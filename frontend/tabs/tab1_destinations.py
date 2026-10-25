"""
tabs/tab1_destinations.py - Smart Destination Recommender.
Nordic / Japandi minimalist redesign.
"""

import streamlit as st
from backend.ai_client import call_ai, build_destination_prompt, extract_json
from backend.config import DEMO_DESTINATIONS


def _render_dest_card(dest: dict, rank: int):
    match = dest.get("match_score", 90)
    bar_pct = match

    # Subtle left-border accent per rank (walnut / sage / terracotta)
    accents = ["#7A5C3D", "#607B68", "#B87050"]
    rank_labels = ["01", "02", "03"]
    accent = accents[rank]

    tags_html = "".join(
        f'<span class="dest-tag">{t}</span>' for t in dest.get("tags", [])
    )

    st.markdown(f"""
<div class="dest-card" style="border-left:3px solid {accent};">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.6rem;">
    <div>
      <div class="dest-card-city">{dest.get('city', 'Unknown')}</div>
      <div style="color:#A89F98;font-size:0.8rem;margin-top:0.1rem;letter-spacing:0.02em;">
        {dest.get('country','')}
      </div>
    </div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:600;
                color:#E4DDD4;line-height:1;user-select:none;">
      {rank_labels[rank]}
    </div>
  </div>
  <div class="dest-card-match">Match — {match}%</div>
  <div class="dest-tags">{tags_html}</div>
  <div class="dest-why">"{dest.get('why','')}"</div>
  <div class="dest-meta">
    <span>Best time: {dest.get('best_time','')}</span>
    <span>~${dest.get('avg_budget_usd',0)} / day</span>
  </div>
  <div style="margin-top:1rem;">
    <div style="display:flex;justify-content:space-between;font-size:0.7rem;
                color:#A89F98;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:0.35rem;">
      <span>Match Score</span><span>{match}%</span>
    </div>
    <div class="budget-bar-bg">
      <div class="budget-bar-fill" style="width:{bar_pct}%;background:{accent};"></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


def render_tab1(prefs: dict):
    st.markdown("""
<div class="section-header">
  <span class="section-icon">◈</span>
  <h2>Destination Recommender</h2>
</div>
<p style="color:#6B6460;margin-bottom:1.75rem;font-size:0.9rem;line-height:1.65;">
  Our AI cross-references your vibe, budget, and travel season to surface destinations that feel made for you.
</p>
""", unsafe_allow_html=True)

    # Check if we have a fixed destination
    fixed_dest = prefs.get("destination", "").strip()
    if fixed_dest:
        st.info(f"You've selected **{fixed_dest}** as your destination. Head to the **Itinerary Generator** tab to build your plan, or clear the destination field in the sidebar to receive AI recommendations.")
        return

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
<div class="card" style="padding:0.85rem 1.25rem;">
  <div style="font-size:0.78rem;color:#A89F98;letter-spacing:0.02em;">
    Searching for —
    <strong style="color:#7A5C3D;">{prefs.get('vibe','Any Vibe')}</strong> ·
    <strong style="color:#607B68;">{prefs.get('budget','Moderate')}</strong> ·
    <strong style="color:#B87050;">{prefs.get('party','Solo')}</strong>
  </div>
</div>
""", unsafe_allow_html=True)

    with col2:
        find_btn = st.button("Find Destinations", use_container_width=True, key="find_dest_btn")

    if find_btn or st.session_state.get("destinations_loaded"):
        if not st.session_state.get("destinations_loaded"):
            with st.spinner("Scanning destinations…"):
                raw = call_ai(build_destination_prompt(prefs))
                if raw == "__DEMO__":
                    destinations = DEMO_DESTINATIONS
                    st.session_state["demo_notice"] = True
                else:
                    parsed = extract_json(raw)
                    destinations = parsed if isinstance(parsed, list) else DEMO_DESTINATIONS
                    st.session_state["demo_notice"] = False
                st.session_state["destinations"] = destinations
                st.session_state["destinations_loaded"] = True

        destinations = st.session_state.get("destinations", DEMO_DESTINATIONS)

        if st.session_state.get("demo_notice"):
            st.markdown("""
<div class="status-pill status-demo" style="margin-bottom:1.25rem;">
  Demo Mode — Add your API key in the sidebar for live AI recommendations
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<p style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;
          color:#A89F98;font-weight:500;margin-bottom:1rem;">
  Top Matches for You
</p>
""", unsafe_allow_html=True)

        for i, dest in enumerate(destinations[:3]):
            _render_dest_card(dest, i)

            city = dest.get("city", "")
            if st.button(f"Select {city} & Build Itinerary →", key=f"select_dest_{i}", use_container_width=True):
                st.session_state["selected_destination"] = city
                st.session_state["prefs"] = {**prefs, "destination": city}
                st.success(f"**{city}** selected — switch to Itinerary Generator to build your plan.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Refresh Recommendations", key="refresh_dest"):
            st.session_state.pop("destinations_loaded", None)
            st.session_state.pop("destinations", None)
            st.rerun()
