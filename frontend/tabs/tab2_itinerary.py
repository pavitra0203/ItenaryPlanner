"""
tabs/tab2_itinerary.py - Day-by-Day Optimized Itinerary Generator.
Nordic / Japandi minimalist redesign.
"""

from __future__ import annotations
import streamlit as st
from backend.ai_client import call_ai, build_itinerary_prompt, extract_json
from backend.config import DEMO_ITINERARY


def _period_class(period: str) -> str:
    return {
        "Morning":       "period-morning",
        "Lunch":         "period-lunch",
        "Lunch Snack":   "period-lunch",
        "Morning Transit":"period-morning",
        "Afternoon":     "period-afternoon",
        "Evening":       "period-evening",
    }.get(period, "period-morning")


def _render_slot(slot: dict):
    period = slot.get("period", "")
    period_cls = _period_class(period)
    st.markdown(f"""
<div class="slot-row">
  <div>
    <div class="slot-time">{slot.get('time','')}</div>
    <span class="slot-period-badge {period_cls}">{period}</span>
  </div>
  <div>
    <div class="slot-activity">{slot.get('activity','')}</div>
    <div class="slot-desc">{slot.get('description','')}</div>
    <div class="slot-tip">↳ {slot.get('tips','')}</div>
  </div>
  <div class="slot-cost">
    <div class="cost-usd">${slot.get('cost_usd',0)}</div>
    <div class="cost-inr">₹{slot.get('cost_inr',0)}</div>
    <div class="cost-local">{slot.get('cost_local','')}</div>
  </div>
</div>
""", unsafe_allow_html=True)


def _render_day(day_data: dict):
    day_num = day_data.get("day", 1)
    theme   = day_data.get("theme", f"Day {day_num}")
    cluster = day_data.get("cluster_area", "")
    day_usd = day_data.get("day_total_usd", 0)
    day_inr = day_data.get("day_total_inr", 0)

    st.markdown(f"""
<div class="day-card">
  <div class="day-header">
    <div>
      <div class="day-title">Day {day_num} — {theme}</div>
      <div style="font-size:0.75rem;color:#A89F98;margin-top:0.2rem;letter-spacing:0.02em;">{cluster}</div>
    </div>
    <div class="day-cluster">Geo-Clustered</div>
  </div>
""", unsafe_allow_html=True)

    for slot in day_data.get("slots", []):
        _render_slot(slot)

    st.markdown(f"""
  <div class="day-footer">
    <span class="day-total-label">Day {day_num} Total</span>
    <span class="day-total-val">${day_usd}</span>
    <span style="color:#A89F98;font-size:0.78rem;">₹{day_inr}</span>
  </div>
</div>
""", unsafe_allow_html=True)


def _render_budget_tracker(itinerary: dict, budget_level: str):
    total_usd = itinerary.get("total_cost_usd", 0)
    total_inr = itinerary.get("total_cost_inr", 0)
    duration  = itinerary.get("duration", 1)
    per_day   = total_usd // duration if duration else total_usd

    limits = {
        "💰 Budget (< $50/day)":    50  * duration,
        "💳 Moderate ($50–150/day)": 150 * duration,
        "💎 Luxury ($150+/day)":     500 * duration,
    }
    limit = limits.get(budget_level, 150 * duration)
    pct   = min(100, int((total_usd / limit) * 100)) if limit else 50

    # Earthy fill colors
    bar_color = "#607B68" if pct < 70 else "#B87050" if pct < 90 else "#8B2E20"

    st.markdown(f"""
<div class="budget-tracker">
  <div class="budget-title">Budget Overview</div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.25rem;">
    <div style="text-align:center;">
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:600;color:#607B68;">${total_usd}</div>
      <div class="stat-label">Total USD</div>
    </div>
    <div style="text-align:center;">
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:600;color:#7A5C3D;">₹{total_inr:,}</div>
      <div class="stat-label">Total INR</div>
    </div>
    <div style="text-align:center;">
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:600;color:#B87050;">${per_day}</div>
      <div class="stat-label">Per Day Avg</div>
    </div>
    <div style="text-align:center;">
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:600;color:#1C1917;">{pct}%</div>
      <div class="stat-label">Budget Used</div>
    </div>
  </div>
  <div class="budget-bar-bg">
    <div class="budget-bar-fill" style="width:{pct}%;background:{bar_color};"></div>
  </div>
  <div class="budget-stats">
    <span>$0</span>
    <span style="color:#A89F98;font-size:0.73rem;font-style:italic;">{itinerary.get('currency_note','')}</span>
    <span>${limit}</span>
  </div>
</div>
""", unsafe_allow_html=True)


def render_tab2(prefs: dict):
    st.markdown("""
<div class="section-header">
  <span class="section-icon">◫</span>
  <h2>Itinerary Generator</h2>
</div>
<p style="color:#6B6460;margin-bottom:1.75rem;font-size:0.9rem;line-height:1.65;">
  Geo-clustered, time-optimized day plans that eliminate backtracking and surface the best local experiences.
</p>
""", unsafe_allow_html=True)

    dest = prefs.get("destination", "").strip() or st.session_state.get("selected_destination", "")
    if not dest:
        st.warning("Please set a **Destination** in the sidebar, or use the **Destination Finder** tab to select one.")
        return

    # Info bar
    st.markdown(f"""
<div class="card" style="padding:0.85rem 1.25rem;display:flex;gap:2rem;flex-wrap:wrap;align-items:center;">
  <span style="font-size:0.88rem;font-weight:600;color:#1C1917;">{dest}</span>
  <span style="color:#A89F98;font-size:0.8rem;">{prefs.get('duration',3)} days</span>
  <span style="color:#A89F98;font-size:0.8rem;">{prefs.get('budget','Moderate')}</span>
  <span style="color:#A89F98;font-size:0.8rem;">{prefs.get('party','Solo')}</span>
  <span style="color:#A89F98;font-size:0.8rem;">{prefs.get('pace','Moderate')}</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        gen_btn = st.button("Generate Itinerary", use_container_width=True, key="gen_itin_btn")
    with col2:
        if st.session_state.get("itinerary"):
            if st.button("Regenerate", use_container_width=True, key="regen_itin_btn"):
                st.session_state.pop("itinerary", None)
                st.rerun()

    if gen_btn or st.session_state.get("itinerary"):
        if not st.session_state.get("itinerary"):
            with st.spinner(f"Crafting your {prefs.get('duration',3)}-day {dest} itinerary…"):
                active_prefs = {**prefs, "destination": dest}
                raw = call_ai(build_itinerary_prompt(active_prefs))
                if raw == "__DEMO__":
                    itinerary = DEMO_ITINERARY.copy()
                    itinerary["duration"] = prefs.get("duration", 3)
                    st.session_state["demo_itin_notice"] = True
                else:
                    parsed = extract_json(raw)
                    itinerary = parsed if isinstance(parsed, dict) and "days" in parsed else DEMO_ITINERARY.copy()
                    st.session_state["demo_itin_notice"] = False
                st.session_state["itinerary"] = itinerary
                st.session_state["itin_prefs"] = active_prefs

        itinerary = st.session_state["itinerary"]

        if st.session_state.get("demo_itin_notice"):
            st.markdown("""
<div class="status-pill status-demo" style="margin-bottom:1.25rem;">
  Demo Mode — Showing sample Lisbon itinerary. Add API key for live AI plans.
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div class="status-pill status-live" style="margin-bottom:1.25rem;">
  Live AI Itinerary Generated
</div>
""", unsafe_allow_html=True)

        _render_budget_tracker(itinerary, prefs.get("budget", "💳 Moderate ($50–150/day)"))

        st.markdown("""
<p style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;
          color:#A89F98;font-weight:500;margin-bottom:1rem;margin-top:1.5rem;">
  Day-by-Day Plan
</p>
""", unsafe_allow_html=True)

        days = itinerary.get("days", [])[:prefs.get("duration", 3)]
        for day_data in days:
            _render_day(day_data)

        st.success("Itinerary ready — head to **Vibe & Swaps** to refine activities, or **Trip Management** to save & export.")
