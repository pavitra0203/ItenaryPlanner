"""
pdf_export.py - Generate a beautifully formatted offline PDF travel itinerary.
Styled according to the project's Modern Minimalist (Nordic / Japandi) design system.
Uses fpdf2 with zero external binary dependencies.
"""

from __future__ import annotations
import io
from datetime import datetime
from fpdf import FPDF
from backend.config import EMERGENCY_CONTACTS, APP_NAME


def clean_for_pdf(text: str) -> str:
    """Sanitize strings to ensure strict compatibility with core Latin-1 PDF fonts."""
    if not text:
        return ""
    text = str(text)
    replacements = {
        "✈": "",
        "₹": "INR ",
        "€": "EUR ",
        "£": "GBP ",
        "—": " - ",
        "–": " - ",
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "•": "*",
        "☐": "[ ]",
        "☑": "[x]",
        "📍": "",
        "💰": "",
        "💡": "Tip: ",
        "🗓": "",
        "🌙": "",
        "👥": "",
        "💵": "",
        "🆘": "",
        "✅": "[x] ",
        "🚔": "",
        "🚑": "",
        "🗺️": "",
        "🏛️": "",
        "⭐": "*",
        "🎯": "",
        "🏃": "",
        "🎨": "",
        "🎒": "",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Ensure all remaining characters are safely encodable in latin-1
    return text.encode("latin-1", "ignore").decode("latin-1")


class ItineraryPDF(FPDF):
    """
    Custom FPDF subclass formatted in the Nordic / Japandi aesthetic:
    warm paper white canvas, walnut woodcraft, matcha sage, terracotta,
    and crisp charcoal typography.
    """

    # Nordic / Japandi Palette
    WALNUT = (120, 84, 56)       # #785438 - Primary Brand
    SAGE = (82, 115, 91)         # #52735B - Matcha Accent
    TERRACOTTA = (179, 101, 62)  # #B3653E - Terracotta Accent
    CHARCOAL = (28, 25, 23)      # #1C1917 - High-contrast text
    STONE = (120, 113, 108)      # #78716C - Muted metadata
    SAND = (247, 245, 240)       # #F7F5F0 - Washi card background
    BORDER = (228, 221, 212)     # #E4DDD4 - Tactile border lines
    WHITE = (255, 255, 255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(14, 14, 14)

    def normalize_text(self, text: str) -> str:
        """Automatically sanitize all text passed to cells/multi-cells."""
        cleaned = clean_for_pdf(text)
        return super().normalize_text(cleaned)

    def header(self):
        # Header only on pages 2 and onward to keep page 1 pristine
        if self.page_no() > 1:
            self.set_fill_color(*self.WALNUT)
            self.rect(14, 8, 182, 1.2, "F")
            self.set_font("Helvetica", "B", 7.5)
            self.set_text_color(*self.STONE)
            self.set_y(10)
            self.cell(0, 4, clean_for_pdf(f"{APP_NAME.upper()}   |   PERSONALIZED TRAVEL ITINERARY"), align="L")
            self.set_draw_color(*self.BORDER)
            self.line(14, 15, 196, 15)
            self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_draw_color(*self.BORDER)
        self.line(14, self.get_y(), 196, self.get_y())
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*self.STONE)
        date_str = datetime.now().strftime("%B %Y")
        self.cell(90, 8, clean_for_pdf(f"Personalized Travel Guide - {date_str}"), align="L")
        self.cell(92, 8, f"Page {self.page_no()}", align="R")


def generate_pdf(itinerary: dict, trip_prefs: dict) -> bytes:
    """
    Generate and return clean, compact PDF bytes for the given itinerary dict.
    Flows continuously without wasteful empty pages.
    """
    pdf = ItineraryPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    # ── Top Decorative Branding Bar ──────────────────────────────────────────
    pdf.set_fill_color(*ItineraryPDF.WALNUT)
    pdf.rect(14, 12, 182, 3.5, "F")
    pdf.set_fill_color(*ItineraryPDF.SAGE)
    pdf.rect(14, 15.5, 60, 1.2, "F")

    # ── Editorial Title Section ──────────────────────────────────────────────
    pdf.set_y(19)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*ItineraryPDF.WALNUT)
    pdf.cell(0, 4, "CURATED EXPEDITION ITINERARY & DESTINATION GUIDE", ln=True)

    dest_name = clean_for_pdf(itinerary.get("destination", "Custom Itinerary"))
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*ItineraryPDF.CHARCOAL)
    pdf.cell(0, 9, dest_name, ln=True)

    # Subtitle
    party = clean_for_pdf(str(trip_prefs.get("party", "Solo Traveler")))
    duration = itinerary.get("duration", len(itinerary.get("days", [])))
    budget = clean_for_pdf(str(trip_prefs.get("budget", "Moderate")))
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*ItineraryPDF.STONE)
    pdf.cell(0, 5, f"{duration} Days  *  {party}  *  {budget} Level", ln=True)
    pdf.ln(2)

    # ── Overview Summary Card ────────────────────────────────────────────────
    start_y = pdf.get_y()
    card_h = 16
    pdf.set_fill_color(*ItineraryPDF.SAND)
    pdf.set_draw_color(*ItineraryPDF.BORDER)
    pdf.rect(14, start_y, 182, card_h, "DF")

    # 4 Columns
    col_w = 182 / 4
    dates_val = clean_for_pdf(trip_prefs.get("dates") or "Flexible Dates")
    pace_val = clean_for_pdf(trip_prefs.get("pace") or "Moderate")
    tot_usd = itinerary.get("total_cost_usd", 0)
    tot_inr = itinerary.get("total_cost_inr", 0)

    overview_cols = [
        ("DATES", dates_val),
        ("PACE / PARTY", f"{pace_val} ({party[:10]})"),
        ("TOTAL EST. (USD)", f"${tot_usd:,}"),
        ("TOTAL EST. (INR)", f"INR {tot_inr:,}"),
    ]

    for i, (label, val) in enumerate(overview_cols):
        col_x = 14 + (i * col_w)
        pdf.set_xy(col_x + 3, start_y + 2.5)
        pdf.set_font("Helvetica", "B", 6.8)
        pdf.set_text_color(*ItineraryPDF.WALNUT)
        pdf.cell(col_w - 6, 4, label)

        pdf.set_xy(col_x + 3, start_y + 7.5)
        pdf.set_font("Helvetica", "B", 8.8)
        pdf.set_text_color(*ItineraryPDF.CHARCOAL)
        pdf.cell(col_w - 6, 5, val)

    pdf.set_y(start_y + card_h + 4)

    # ── Sequential Day Plans (Continuous Flow) ───────────────────────────────
    days = itinerary.get("days", [])
    period_colors = {
        "Morning": ItineraryPDF.TERRACOTTA,
        "Lunch": ItineraryPDF.SAGE,
        "Afternoon": ItineraryPDF.WALNUT,
        "Evening": (50, 45, 40),
    }

    for day in days:
        # Check if remaining space is too small for header + 1 slot (need ~40mm)
        if pdf.get_y() > 240:
            pdf.add_page()

        day_num = day.get("day", 1)
        theme = clean_for_pdf(day.get("theme", f"Day {day_num}"))
        cluster = clean_for_pdf(day.get("cluster_area", "Local Area"))
        day_usd = day.get("day_total_usd", 0)
        day_inr = day.get("day_total_inr", 0)

        # Day Header Bar
        hy = pdf.get_y()
        pdf.set_fill_color(*ItineraryPDF.WALNUT)
        pdf.rect(14, hy, 182, 6.8, "F")
        pdf.set_xy(16, hy + 1.2)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*ItineraryPDF.WHITE)
        pdf.cell(120, 4.5, f"DAY {day_num} : {theme.upper()}")

        # Daily budget right-aligned in header
        pdf.set_xy(136, hy + 1.2)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(58, 4.5, f"${day_usd}  |  INR {day_inr:,}", align="R")

        # Cluster Sub-bar
        pdf.set_y(hy + 7.5)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(*ItineraryPDF.STONE)
        pdf.cell(0, 4, f"Cluster Area: {cluster}", ln=True)
        pdf.ln(1)

        # Render Slots
        for slot in day.get("slots", []):
            if pdf.get_y() > 255:
                pdf.add_page()

            period = slot.get("period", "Activity")
            p_color = period_colors.get(period, ItineraryPDF.WALNUT)
            time_str = clean_for_pdf(slot.get("time", ""))
            activity = clean_for_pdf(slot.get("activity", "Activity"))
            description = clean_for_pdf(slot.get("description", ""))
            tips = clean_for_pdf(slot.get("tips", ""))

            slot_usd = slot.get("cost_usd", 0)
            slot_inr = slot.get("cost_inr", 0)

            sy = pdf.get_y()
            # Left vertical accent line
            pdf.set_fill_color(*p_color)
            pdf.rect(14, sy, 1.8, 11, "F")

            # Period Badge
            pdf.set_xy(18, sy)
            pdf.set_fill_color(*p_color)
            pdf.set_text_color(*ItineraryPDF.WHITE)
            pdf.set_font("Helvetica", "B", 7)
            badge_text = f" {period.upper()} "
            pdf.cell(20, 4, badge_text, fill=True)

            # Time
            pdf.set_font("Helvetica", "", 7.5)
            pdf.set_text_color(*ItineraryPDF.STONE)
            pdf.cell(45, 4, f"  {time_str}")

            # Cost (Right aligned)
            cost_label = f"${slot_usd}"
            if slot_inr:
                cost_label += f"  (INR {slot_inr:,})"
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.set_text_color(*ItineraryPDF.SAGE)
            pdf.cell(0, 4, cost_label, align="R", ln=True)

            # Activity Name
            pdf.set_x(18)
            pdf.set_font("Helvetica", "B", 8.8)
            pdf.set_text_color(*ItineraryPDF.CHARCOAL)
            pdf.cell(0, 4.5, activity, ln=True)

            # Description
            if description:
                pdf.set_x(18)
                pdf.set_font("Helvetica", "", 7.8)
                pdf.set_text_color(*ItineraryPDF.CHARCOAL)
                pdf.multi_cell(176, 3.8, description)

            # Tip
            if tips:
                pdf.set_x(18)
                pdf.set_font("Helvetica", "I", 7.2)
                pdf.set_text_color(*ItineraryPDF.TERRACOTTA)
                pdf.cell(0, 3.6, f"Tip: {tips}", ln=True)

            pdf.ln(2)

        pdf.ln(2.5)

    # ── Final Section: Budget Table & Safety / Checklist ─────────────────────
    if pdf.get_y() > 165:
        pdf.add_page()
    else:
        pdf.ln(3)

    sec_y = pdf.get_y()
    pdf.set_fill_color(*ItineraryPDF.WALNUT)
    pdf.rect(14, sec_y, 182, 6, "F")
    pdf.set_xy(16, sec_y + 1)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(*ItineraryPDF.WHITE)
    pdf.cell(0, 4, "TRIP BUDGET BREAKDOWN & LOGISTICS")
    pdf.set_y(sec_y + 8)

    # Budget Table Header
    pdf.set_fill_color(*ItineraryPDF.SAND)
    pdf.set_draw_color(*ItineraryPDF.BORDER)
    pdf.set_text_color(*ItineraryPDF.WALNUT)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.cell(14, 5, "DAY", border=1, fill=True)
    pdf.cell(98, 5, "THEME & HIGHLIGHTS", border=1, fill=True)
    pdf.cell(35, 5, "EST. USD", border=1, fill=True, align="R")
    pdf.cell(35, 5, "EST. INR", border=1, fill=True, align="R", ln=True)

    running_usd = 0
    running_inr = 0
    for i, d in enumerate(days):
        day_cost_usd = d.get("day_total_usd", 0)
        day_cost_inr = d.get("day_total_inr", 0)
        running_usd += day_cost_usd
        running_inr += day_cost_inr

        bg = ItineraryPDF.WHITE if i % 2 == 0 else ItineraryPDF.SAND
        pdf.set_fill_color(*bg)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(*ItineraryPDF.CHARCOAL)
        pdf.cell(14, 4.5, f"Day {d.get('day', i+1)}", border=1, fill=True)
        pdf.cell(98, 4.5, clean_for_pdf(d.get("theme", "")[:50]), border=1, fill=True)
        pdf.set_text_color(*ItineraryPDF.SAGE)
        pdf.cell(35, 4.5, f"${day_cost_usd}", border=1, fill=True, align="R")
        pdf.cell(35, 4.5, f"INR {day_cost_inr:,}", border=1, fill=True, align="R", ln=True)

    # Total row
    pdf.set_fill_color(*ItineraryPDF.WALNUT)
    pdf.set_text_color(*ItineraryPDF.WHITE)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(112, 5, "TOTAL TRIP ESTIMATE", border=1, fill=True)
    pdf.cell(35, 5, f"${running_usd:,}", border=1, fill=True, align="R")
    pdf.cell(35, 5, f"INR {running_inr:,}", border=1, fill=True, align="R", ln=True)

    currency_note = clean_for_pdf(itinerary.get("currency_note", ""))
    if currency_note:
        pdf.set_font("Helvetica", "I", 6.8)
        pdf.set_text_color(*ItineraryPDF.STONE)
        pdf.cell(0, 4, currency_note, ln=True)

    pdf.ln(3)

    # ── Emergency Contacts & Checklist (Compact 2-Column) ────────────────────
    if pdf.get_y() > 220:
        pdf.add_page()

    two_col_y = pdf.get_y()
    left_w = 85
    right_w = 93

    # Left Column: Emergency Contacts
    pdf.set_xy(14, two_col_y)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*ItineraryPDF.WALNUT)
    pdf.cell(left_w, 4.5, "EMERGENCY CONTACTS", ln=True)

    dest = itinerary.get("destination", "")
    country_key = "Default"
    for country in EMERGENCY_CONTACTS:
        if country.lower() in dest.lower():
            country_key = country
            break
    contacts = EMERGENCY_CONTACTS.get(country_key, EMERGENCY_CONTACTS["Default"])

    contact_items = [
        ("Police / Emergency", contacts.get("police", "112 / 911")),
        ("Ambulance", contacts.get("ambulance", "112 / 911")),
        ("Tourist Police", contacts.get("tourist_police", "Contact local office")),
        ("US Embassy", contacts.get("embassy_us", "www.usembassy.gov")),
    ]

    pdf.set_font("Helvetica", "", 7.5)
    for lbl, val in contact_items:
        pdf.set_x(14)
        pdf.set_text_color(*ItineraryPDF.STONE)
        pdf.cell(35, 4, clean_for_pdf(lbl))
        pdf.set_text_color(*ItineraryPDF.CHARCOAL)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.cell(left_w - 35, 4, clean_for_pdf(val), ln=True)
        pdf.set_font("Helvetica", "", 7.5)

    # Right Column: Pre-Travel Checklist
    pdf.set_xy(14 + left_w + 4, two_col_y)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*ItineraryPDF.WALNUT)
    pdf.cell(right_w, 4.5, "PRE-TRAVEL CHECKLIST", ln=True)

    checklist_items = [
        "Passport valid 6+ months with copies saved",
        "Travel insurance policy noted & active",
        "Accommodation & flight tickets offline",
        "Local currency & backup card configured",
        "Important prescriptions & first aid packed",
        "Offline maps downloaded (Google Maps / Maps.me)",
    ]

    pdf.set_font("Helvetica", "", 7.2)
    pdf.set_text_color(*ItineraryPDF.CHARCOAL)
    for item in checklist_items:
        pdf.set_x(14 + left_w + 4)
        pdf.cell(right_w, 3.8, f"[ ]  {item}", ln=True)

    pdf_output = pdf.output(dest="S")
    if isinstance(pdf_output, str):
        return pdf_output.encode("latin-1")
    return bytes(pdf_output)
