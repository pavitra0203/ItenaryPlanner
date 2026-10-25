"""
tabs/tab3_vibe.py - Vibe Customization & Dynamic Activity Swap.
Nordic / Japandi minimalist redesign.
"""

from __future__ import annotations
import streamlit as st
from backend.ai_client import call_ai, build_swap_prompt, extract_json
from backend.config import DEMO_ITINERARY


SWAP_SUGGESTIONS = {
    "Morning": [
        "Swap museum for outdoor market",
        "Find a sunrise viewpoint instead",
        "Replace with a cooking class",
        "Add a guided walking tour",
    ],
    "Lunch": [
        "Find vegetarian / vegan lunch spot",
        "Find a rooftop restaurant",
        "Street food experience instead",
        "Budget-friendly local café",
    ],
    "Afternoon": [
        "Swap to water activity / boat tour",
        "Add a wine or brewery tasting",
        "Replace with spa & wellness",
        "Find a local art gallery",
    ],
    "Evening": [
        "Add live music venue",
        "Find a food / night market",
        "Swap to rooftop bar",
        "Quiet neighbourhood evening walk",
    ],
}


def _period_class(period: str) -> str:
    return {
        "Morning":        "period-morning",
        "Lunch":          "period-lunch",
        "Lunch Snack":    "period-lunch",
        "Morning Transit":"period-morning",
        "Afternoon":      "period-afternoon",
        "Evening":        "period-evening",
    }.get(period, "period-morning")


def _render_slot_compact(slot: dict):
    period = slot.get("period", "")
    period_cls = _period_class(period)
    st.markdown(f"""
<div style="display:flex;gap:1rem;align-items:flex-start;padding:0.8rem 0;
            border-bottom:1px solid #F0EDE6;">
  <div style="min-width:105px;">
    <div style="font-size:0.72rem;color:#A89F98;font-weight:500;letter-spacing:0.02em;">
      {slot.get('time','')}
    </div>
    <span class="slot-period-badge {period_cls}" style="margin-top:0.3rem;display:inline-block;">
      {period}
    </span>
  </div>
  <div style="flex:1;">
    <div style="font-weight:600;color:#1C1917;font-size:0.92rem;">{slot.get('activity','')}</div>
    <div style="color:#6B6460;font-size:0.8rem;margin-top:0.15rem;line-height:1.55;">
      {slot.get('description','')[:130]}…
    </div>
  </div>
  <div style="text-align:right;min-width:65px;">
    <div style="font-weight:700;color:#607B68;font-size:0.9rem;">${slot.get('cost_usd',0)}</div>
    <div style="color:#A89F98;font-size:0.72rem;">₹{slot.get('cost_inr',0)}</div>
  </div>
</div>
""", unsafe_allow_html=True)


def render_tab3(prefs: dict):
    st.markdown("""
<div class="section-header">
  <span class="section-icon">◧</span>
  <h2>Vibe & Activity Swap</h2>
</div>
<p style="color:#6B6460;margin-bottom:1.75rem;font-size:0.9rem;line-height:1.65;">
  Fine-tune individual time slots without regenerating the entire plan. Swap, replace, or personalise one activity at a time.
</p>
""", unsafe_allow_html=True)

    itinerary = st.session_state.get("itinerary")
    if not itinerary:
        st.warning("No itinerary loaded. Generate one in the **Itinerary Generator** tab first.")
        if st.button("Load Demo Itinerary for Preview", key="load_demo_tab3"):
            st.session_state["itinerary"] = DEMO_ITINERARY.copy()
            st.session_state["itin_prefs"] = prefs
            st.rerun()
        return

    itin_prefs = st.session_state.get("itin_prefs", prefs)
    days = itinerary.get("days", [])[:prefs.get("duration", 3)]

    # ── Swap Panel ────────────────────────────────────────────────────────────
    st.markdown("""
<p style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;
          color:#A89F98;font-weight:500;margin-bottom:1rem;">Swap Control Panel</p>
""", unsafe_allow_html=True)

    swap_col1, swap_col2 = st.columns([1, 1])

    with swap_col1:
        day_options = [f"Day {d['day']} — {d.get('theme','')}" for d in days]
        selected_day_label = st.selectbox("Select Day", day_options, key="swap_day_select")
        day_idx = day_options.index(selected_day_label)
        selected_day_data = days[day_idx]

    with swap_col2:
        slot_options = [
            f"{s.get('period','')} — {s.get('activity','')[:30]}"
            for s in selected_day_data.get("slots", [])
        ]
        selected_slot_label = st.selectbox("Select Slot", slot_options, key="swap_slot_select")
        slot_idx = slot_options.index(selected_slot_label)
        selected_slot = selected_day_data["slots"][slot_idx]

    st.markdown("<p style='font-size:0.78rem;color:#A89F98;margin-bottom:0.4rem;'>Current Activity</p>", unsafe_allow_html=True)
    _render_slot_compact(selected_slot)

    # Quick suggestions
    period = selected_slot.get("period", "Morning")
    suggestions = SWAP_SUGGESTIONS.get(period, SWAP_SUGGESTIONS["Morning"])

    st.markdown("<p style='font-size:0.78rem;color:#A89F98;margin-top:1rem;margin-bottom:0.5rem;'>Quick Suggestions</p>", unsafe_allow_html=True)
    sug_cols = st.columns(len(suggestions))
    chosen_sug = ""
    for i, sug in enumerate(suggestions):
        with sug_cols[i]:
            if st.button(sug, key=f"sug_{day_idx}_{slot_idx}_{i}", use_container_width=True):
                chosen_sug = sug

    swap_request = st.text_input(
        "Describe your preferred swap:",
        value=chosen_sug,
        placeholder='e.g. "Find a vegetarian lunch spot with garden seating"',
        key="custom_swap_input",
        label_visibility="visible",
    )

    do_swap = st.button("Apply Swap", key="apply_swap_btn", use_container_width=False)

    if do_swap and swap_request.strip():
        with st.spinner(f"Finding the ideal replacement…"):
            raw = call_ai(build_swap_prompt(itin_prefs, selected_day_data["day"], period, swap_request))
            if raw == "__DEMO__":
                new_slot = {
                    **selected_slot,
                    "activity": f"{swap_request[:45]}",
                    "description": f"A curated alternative based on your request. Keeps you in the same cluster with minimal added transit.",
                    "tips": "Reserve in advance where possible.",
                    "cost_usd": selected_slot.get("cost_usd", 20),
                    "cost_inr": selected_slot.get("cost_inr", 1670),
                }
                demo_notice = True
            else:
                parsed = extract_json(raw)
                new_slot = parsed if isinstance(parsed, dict) and "activity" in parsed else selected_slot
                demo_notice = False

        itin = st.session_state["itinerary"]
        itin["days"][day_idx]["slots"][slot_idx] = new_slot
        st.session_state["itinerary"] = itin
        st.success(f"Swapped **{period}** on Day {selected_day_data['day']}.")
        if demo_notice:
            st.info("Demo mode active — add an API key for AI-powered smart swaps.")
        st.rerun()

    st.markdown("<div style='border-top:1px solid #E4DDD4;margin:2rem 0;'></div>", unsafe_allow_html=True)

    # ── Itinerary Overview ────────────────────────────────────────────────────
    st.markdown("""
<p style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;
          color:#A89F98;font-weight:500;margin-bottom:1rem;">Full Itinerary Overview</p>
""", unsafe_allow_html=True)

    for day_data in days:
        with st.expander(
            f"Day {day_data['day']}  ·  {day_data.get('theme','')}  ·  {day_data.get('cluster_area','')}  ·  ${day_data.get('day_total_usd',0)}",
            expanded=False
        ):
            for slot in day_data.get("slots", []):
                _render_slot_compact(slot)

    st.markdown("<div style='border-top:1px solid #E4DDD4;margin:2rem 0;'></div>", unsafe_allow_html=True)

    # ── Vibe Sliders ──────────────────────────────────────────────────────────
    st.markdown("""
<p style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;
          color:#A89F98;font-weight:500;margin-bottom:0.75rem;">Trip Personality</p>
<p style="color:#6B6460;font-size:0.82rem;margin-bottom:1rem;">
  Adjust to reflect your ideal pace (visual feedback only — use Swap above to regenerate activities).
</p>
""", unsafe_allow_html=True)

    v_col1, v_col2, v_col3 = st.columns(3)
    with v_col1:
        adventure = st.slider("Adventure", 1, 10, 5, key="vibe_adventure")
    with v_col2:
        food = st.slider("Foodie Focus", 1, 10, 7, key="vibe_food")
    with v_col3:
        culture = st.slider("Cultural Depth", 1, 10, 6, key="vibe_culture")

    total_vibe = adventure + food + culture
    vibe_label = "Slow & Intentional" if total_vibe < 15 else "Balanced Explorer" if total_vibe < 22 else "Full Immersion"
    vibe_color = "#607B68" if total_vibe < 15 else "#7A5C3D" if total_vibe < 22 else "#B87050"

    st.markdown(f"""
<div class="card" style="text-align:center;padding:1.25rem;">
  <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;font-weight:600;
              color:{vibe_color};margin-bottom:0.3rem;">{vibe_label}</div>
  <div style="color:#A89F98;font-size:0.78rem;letter-spacing:0.03em;">
    Adventure {adventure}/10  ·  Foodie {food}/10  ·  Culture {culture}/10
  </div>
</div>
""", unsafe_allow_html=True)
