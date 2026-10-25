"""
tabs/tab4_management.py - Trip Management & Offline PDF Export.
Nordic / Japandi minimalist redesign.
"""

from __future__ import annotations
from datetime import datetime
import streamlit as st
from backend.trip_db import save_trip, get_all_trips, delete_trip, clear_all_trips, get_trip
from backend.pdf_export import generate_pdf
from backend.config import DEMO_ITINERARY


def _trip_card_html(trip: dict) -> str:
    dest = trip.get("destination", "Unknown")
    dur = trip.get("duration", 0)
    party = trip.get("party", "Solo")
    budget = trip.get("budget", "Moderate")
    dates = f" · {trip['dates']}" if trip.get("dates") else ""
    cost = trip.get("total_cost_usd", 0)
    created = trip.get("created_at", "")
    trip_id = trip.get("id", "")

    return (
        f'<div class="trip-hist-card">'
        f'<div style="flex:1;">'
        f'<div class="trip-hist-dest">{dest}</div>'
        f'<div class="trip-hist-meta">{dur} days · {party} · {budget}{dates}</div>'
        f'<div class="trip-hist-meta" style="margin-top:0.2rem;color:#607B68;">Est. ${cost} · Saved {created}</div>'
        f'</div>'
        f'<div><span class="trip-hist-badge">#{trip_id}</span></div>'
        f'</div>'
    )


def render_tab4(prefs: dict):
    st.markdown("""
<div class="section-header">
  <span class="section-icon">▣</span>
  <h2>Trip Management &amp; PDF Export</h2>
</div>
<p style="color:#6B6460;margin-bottom:1.75rem;font-size:0.9rem;line-height:1.65;">
  Save itineraries, browse your travel archive, and export beautifully formatted offline PDF guides.
</p>
""", unsafe_allow_html=True)

    itinerary = st.session_state.get("itinerary")

    # ── Save Current Trip ─────────────────────────────────────────────────────
    st.markdown("<p style='font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:#A89F98;font-weight:500;margin-bottom:1rem;'>Current Trip</p>", unsafe_allow_html=True)

    if not itinerary:
        st.warning("No active itinerary found. Generate one in the **Itinerary Generator** tab first, or load a demo below.")
        load_col1, load_col2 = st.columns(2)
        with load_col1:
            if st.button("Load Demo Itinerary", use_container_width=True):
                st.session_state["itinerary"] = DEMO_ITINERARY.copy()
                st.session_state["itin_prefs"] = prefs
                st.rerun()
    else:
        dest  = itinerary.get("destination", "Unknown")
        dur   = itinerary.get("duration", 0)
        total = itinerary.get("total_cost_usd", 0)

        st.markdown(
            f'<div class="card" style="padding:1rem 1.4rem;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">'
            f'<div>'
            f'<div style="font-size:1rem;font-weight:600;color:#1C1917;">{dest}</div>'
            f'<div style="color:#A89F98;font-size:0.8rem;margin-top:0.15rem;">{dur} days · {prefs.get("party","Solo")} · Est. ${total}</div>'
            f'</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        action_col1, action_col2 = st.columns(2)

        with action_col1:
            if st.button("Save to Trip History", use_container_width=True, key="save_trip_btn"):
                itin_prefs = st.session_state.get("itin_prefs", prefs)
                trip_id = save_trip(itinerary, itin_prefs)
                st.success(f"Trip saved — ID: **#{trip_id}**")

        with action_col2:
            try:
                itin_prefs = st.session_state.get("itin_prefs", prefs)
                pdf_bytes = generate_pdf(itinerary, itin_prefs)
                dest_slug = dest.replace(",", "").replace(" ", "_").lower()
                filename  = f"itinerary_{dest_slug}_{datetime.now().strftime('%Y%m%d')}.pdf"
                st.download_button(
                    label="Download PDF Guide",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_pdf_btn",
                )
            except Exception as exc:
                st.error(f"PDF generation error: {exc}")

    st.markdown("<div style='border-top:1px solid #E4DDD4;margin:2rem 0;'></div>", unsafe_allow_html=True)

    # ── Trip History ──────────────────────────────────────────────────────────
    st.markdown("<p style='font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:#A89F98;font-weight:500;margin-bottom:1rem;'>Saved Trips</p>", unsafe_allow_html=True)

    trips = get_all_trips()

    if not trips:
        st.markdown("""
<div class="card" style="text-align:center;padding:2rem;">
  <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;color:#E4DDD4;margin-bottom:0.5rem;">✈</div>
  <div style="font-size:1rem;color:#6B6460;">No saved trips yet.</div>
  <div style="font-size:0.82rem;color:#A89F98;margin-top:0.3rem;">
    Generate an itinerary and save it to start building your travel archive.
  </div>
</div>
""", unsafe_allow_html=True)
    else:
        total_destinations = len(trips)
        total_days  = sum(t.get("duration", 0) for t in trips)
        total_spend = sum(t.get("total_cost_usd", 0) for t in trips)

        stat_cols = st.columns(3)
        with stat_cols[0]:
            st.metric("Trips Planned", total_destinations)
        with stat_cols[1]:
            st.metric("Total Days", total_days)
        with stat_cols[2]:
            st.metric("Est. Total Spend", f"${total_spend}")

        st.markdown("<br>", unsafe_allow_html=True)

        for i, trip in enumerate(trips):
            st.markdown(_trip_card_html(trip), unsafe_allow_html=True)

            action_cols = st.columns([2, 2, 1])

            with action_cols[0]:
                try:
                    pdf_bytes = generate_pdf(trip["itinerary"], trip["prefs"])
                    dest_slug = trip["destination"].replace(",", "").replace(" ", "_").lower()
                    filename  = f"itinerary_{dest_slug}_{trip['id']}.pdf"
                    st.download_button(
                        label="Download PDF",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True,
                        key=f"dl_pdf_{trip['id']}_{i}",
                    )
                except Exception:
                    st.caption("PDF unavailable")

            with action_cols[1]:
                if st.button("Restore to Active", key=f"restore_{trip['id']}_{i}", use_container_width=True):
                    st.session_state["itinerary"] = trip["itinerary"]
                    st.session_state["itin_prefs"] = trip["prefs"]
                    st.success(f"Trip **{trip['destination']}** restored to active session.")
                    st.rerun()

            with action_cols[2]:
                if st.button("×", key=f"del_{trip['id']}_{i}", help=f"Delete trip #{trip['id']}"):
                    delete_trip(trip["id"])
                    st.success("Trip deleted.")
                    st.rerun()

            st.markdown("<div style='margin-bottom:0.4rem;'></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear All Trip History", key="clear_all_trips"):
            clear_all_trips()
            st.warning("All trip history cleared.")
            st.rerun()

    st.markdown("<div style='border-top:1px solid #E4DDD4;margin:2rem 0;'></div>", unsafe_allow_html=True)

    # ── Emergency Contacts ────────────────────────────────────────────────────
    st.markdown("<p style='font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:#A89F98;font-weight:500;margin-bottom:0.5rem;'>Emergency Contacts</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B6460;font-size:0.82rem;margin-bottom:1rem;'>Included automatically in every exported PDF guide.</p>", unsafe_allow_html=True)

    from backend.config import EMERGENCY_CONTACTS
    dest_active = ""
    if itinerary:
        dest_active = itinerary.get("destination", "")
    elif trips:
        dest_active = trips[0].get("destination", "")

    country_key = "Default"
    for country in EMERGENCY_CONTACTS:
        if country.lower() in dest_active.lower():
            country_key = country
            break
    contacts = EMERGENCY_CONTACTS.get(country_key, EMERGENCY_CONTACTS["Default"])

    contact_cols = st.columns(2)
    contact_items = [
        ("Police / Emergency", contacts["police"]),
        ("Ambulance",          contacts["ambulance"]),
        ("Tourist Police",     contacts["tourist_police"]),
        ("US Embassy",         contacts["embassy_us"]),
    ]
    for i, (label, val) in enumerate(contact_items):
        with contact_cols[i % 2]:
            st.markdown(f"""
<div class="card" style="padding:0.8rem 1.2rem;margin-bottom:0.5rem;">
  <div class="stat-label" style="margin-bottom:0.2rem;">{label}</div>
  <div style="font-size:0.95rem;font-weight:600;color:#7A5C3D;">{val}</div>
</div>
""", unsafe_allow_html=True)

    # ── Pre-Travel Checklist ──────────────────────────────────────────────────
    st.markdown("<div style='border-top:1px solid #E4DDD4;margin:2rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:#A89F98;font-weight:500;margin-bottom:1rem;'>Pre-Travel Checklist</p>", unsafe_allow_html=True)

    checklist_items = [
        "Passport valid for 6+ months",
        "Travel insurance purchased",
        "Accommodation confirmed",
        "Flights / transport downloaded offline",
        "Local currency / ATM plan ready",
        "Medications packed with prescriptions",
        "International SIM / data plan activated",
        "Emergency contacts saved in phone",
        "Document copies in cloud storage",
        "Bank notified of travel dates",
        "Offline maps downloaded",
        "Visa requirements verified",
    ]
    if "checklist_state" not in st.session_state:
        st.session_state["checklist_state"] = {item: False for item in checklist_items}

    chk_col1, chk_col2 = st.columns(2)
    for i, item in enumerate(checklist_items):
        col = chk_col1 if i % 2 == 0 else chk_col2
        with col:
            checked = st.checkbox(
                item,
                value=st.session_state["checklist_state"].get(item, False),
                key=f"chk_{i}",
            )
            st.session_state["checklist_state"][item] = checked

    checked_count = sum(1 for v in st.session_state["checklist_state"].values() if v)
    total_items   = len(checklist_items)
    pct           = int((checked_count / total_items) * 100)
    pct_color     = "#607B68" if pct == 100 else "#B87050" if pct > 50 else "#A89F98"

    st.markdown(f"""
<div style="margin-top:1rem;">
  <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#A89F98;
              text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.4rem;">
    <span>Travel Ready — {checked_count} of {total_items}</span>
    <span style="color:{pct_color};font-weight:600;">{pct}%</span>
  </div>
  <div class="budget-bar-bg">
    <div class="budget-bar-fill" style="width:{pct}%;background:{pct_color};"></div>
  </div>
  {'<div style="color:#607B68;font-weight:500;font-size:0.85rem;margin-top:0.6rem;">You are fully travel-ready.</div>' if pct == 100 else ''}
</div>
""", unsafe_allow_html=True)
