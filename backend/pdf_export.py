"""
pdf_export.py - Generate a beautifully formatted offline PDF travel itinerary.
Uses fpdf2 (no external database required).
"""

from __future__ import annotations
import io
from datetime import datetime
from fpdf import FPDF
from backend.config import EMERGENCY_CONTACTS, APP_NAME


class ItineraryPDF(FPDF):
    """Custom FPDF subclass with branded header/footer."""

    PURPLE = (99, 102, 241)
    PINK = (236, 72, 153)
    DARK = (15, 20, 40)
    LIGHT_GRAY = (148, 163, 184)
    WHITE = (241, 245, 249)
    GREEN = (74, 222, 128)
    ORANGE = (251, 146, 60)

    def header(self):
        # Gradient-style top bar
        self.set_fill_color(*self.PURPLE)
        self.rect(0, 0, 210, 8, "F")
        # App name
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.WHITE)
        self.set_y(10)
        self.cell(0, 6, APP_NAME.upper(), align="C", ln=True)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*self.LIGHT_GRAY)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_title(self, title: str, subtitle: str = ""):
        self.set_fill_color(*self.PURPLE)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 10, title, ln=True, fill=True)
        if subtitle:
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(*self.LIGHT_GRAY)
            self.cell(0, 6, subtitle, ln=True)
        self.ln(3)

    def day_header(self, day_num: int, theme: str, cluster: str, total_usd: int):
        self.set_fill_color(30, 40, 70)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, f"  Day {day_num}  —  {theme}", ln=True, fill=True)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.LIGHT_GRAY)
        self.cell(0, 5, f"  📍 {cluster}   💰 Day total: ${total_usd}", ln=True)
        self.ln(2)

    def slot_row(self, slot: dict):
        period_colors = {
            "Morning": self.ORANGE,
            "Afternoon": self.PURPLE,
            "Evening": self.PINK,
            "Lunch": self.GREEN,
        }
        period = slot.get("period", "Morning")
        color = period_colors.get(period, self.LIGHT_GRAY)

        # Period badge
        self.set_fill_color(*color)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 8)
        self.cell(28, 5, f" {slot.get('emoji','⭐')} {period}", fill=True, border=0)
        self.set_text_color(*self.LIGHT_GRAY)
        self.set_font("Helvetica", "", 8)
        self.cell(0, 5, slot.get("time", ""), ln=True)

        # Activity name
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.WHITE)
        self.set_x(14)
        self.cell(0, 6, slot.get("activity", ""), ln=True)

        # Description
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*self.LIGHT_GRAY)
        self.set_x(14)
        self.multi_cell(170, 5, slot.get("description", ""))

        # Cost row
        self.set_x(14)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.GREEN)
        self.cell(35, 5, f"${slot.get('cost_usd', 0)}")
        self.set_text_color(*self.LIGHT_GRAY)
        self.set_font("Helvetica", "", 8)
        self.cell(35, 5, f"₹{slot.get('cost_inr', 0)}")
        self.cell(0, 5, slot.get("cost_local", ""), ln=True)

        # Tip
        self.set_x(14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(251, 191, 36)  # amber
        self.multi_cell(170, 4.5, f"💡 {slot.get('tips', '')}")
        self.ln(4)

    def section_divider(self):
        self.set_draw_color(*self.PURPLE)
        self.set_line_width(0.5)
        self.line(14, self.get_y(), 196, self.get_y())
        self.ln(4)


def generate_pdf(itinerary: dict, trip_prefs: dict) -> bytes:
    """
    Generate and return PDF bytes for the given itinerary dict.
    """
    pdf = ItineraryPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(14, 24, 14)

    # ── Cover Page ──────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(10, 14, 26)
    pdf.rect(0, 0, 210, 297, "F")

    # Decorative top band
    pdf.set_fill_color(*ItineraryPDF.PURPLE)
    pdf.rect(0, 0, 210, 40, "F")

    pdf.set_y(10)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "✈ TRAVEL ITINERARY", align="C", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(200, 200, 220)
    pdf.cell(0, 7, APP_NAME, align="C", ln=True)

    # Destination box
    pdf.set_y(55)
    pdf.set_font("Helvetica", "B", 30)
    pdf.set_text_color(167, 139, 250)  # purple
    pdf.cell(0, 14, itinerary.get("destination", ""), align="C", ln=True)

    # Trip meta
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(148, 163, 184)
    meta_lines = [
        f"🗓  {trip_prefs.get('dates', 'Dates TBD')}",
        f"🌙  {itinerary.get('duration', '?')} Days",
        f"👥  {trip_prefs.get('party', 'Solo')}",
        f"💰  {trip_prefs.get('budget', 'Moderate')}",
        f"💵  Est. Total: ${itinerary.get('total_cost_usd', 0)}  (₹{itinerary.get('total_cost_inr', 0)})",
    ]
    pdf.ln(8)
    for line in meta_lines:
        pdf.cell(0, 8, line, align="C", ln=True)

    # Generated timestamp
    pdf.set_y(-40)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 6, f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", align="C", ln=True)
    pdf.cell(0, 6, itinerary.get("currency_note", ""), align="C", ln=True)

    # ── Day Pages ────────────────────────────────────────────────────────────
    for day_data in itinerary.get("days", []):
        pdf.add_page()
        pdf.set_fill_color(10, 14, 26)
        pdf.rect(0, 0, 210, 297, "F")

        pdf.day_header(
            day_data["day"],
            day_data.get("theme", f"Day {day_data['day']}"),
            day_data.get("cluster_area", ""),
            day_data.get("day_total_usd", 0),
        )
        pdf.section_divider()

        for slot in day_data.get("slots", []):
            pdf.slot_row(slot)

        # Day cost summary
        pdf.set_fill_color(30, 40, 70)
        pdf.set_text_color(*ItineraryPDF.WHITE)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(0, 7,
                 f"  Day {day_data['day']} Total:  ${day_data.get('day_total_usd', 0)}  |  ₹{day_data.get('day_total_inr', 0)}",
                 fill=True, ln=True)

    # ── Budget Summary Page ──────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(10, 14, 26)
    pdf.rect(0, 0, 210, 297, "F")

    pdf.chapter_title("💰 Budget Summary", "Itemized cost tracker across all days")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*ItineraryPDF.LIGHT_GRAY)

    # Table header
    pdf.set_fill_color(*ItineraryPDF.PURPLE)
    pdf.set_text_color(*ItineraryPDF.WHITE)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(15, 7, "Day", fill=True, border=0)
    pdf.cell(80, 7, "Theme", fill=True, border=0)
    pdf.cell(35, 7, "USD", fill=True, border=0)
    pdf.cell(42, 7, "INR", fill=True, ln=True, border=0)

    running_usd = 0
    running_inr = 0
    for i, day_data in enumerate(itinerary.get("days", [])):
        running_usd += day_data.get("day_total_usd", 0)
        running_inr += day_data.get("day_total_inr", 0)
        fill = i % 2 == 0
        bg = (18, 25, 45) if fill else (13, 18, 35)
        pdf.set_fill_color(*bg)
        pdf.set_text_color(*ItineraryPDF.WHITE)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(15, 6, f"{day_data['day']}", fill=True)
        pdf.cell(80, 6, day_data.get("theme", "")[:38], fill=True)
        pdf.set_text_color(*ItineraryPDF.GREEN)
        pdf.cell(35, 6, f"${day_data.get('day_total_usd', 0)}", fill=True)
        pdf.set_text_color(167, 139, 250)
        pdf.cell(42, 6, f"₹{day_data.get('day_total_inr', 0)}", fill=True, ln=True)

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(*ItineraryPDF.PURPLE)
    pdf.set_text_color(*ItineraryPDF.WHITE)
    pdf.cell(95, 8, "  TOTAL TRIP COST", fill=True)
    pdf.set_text_color(*ItineraryPDF.GREEN)
    pdf.cell(35, 8, f"${running_usd}", fill=True)
    pdf.set_text_color(167, 139, 250)
    pdf.cell(42, 8, f"₹{running_inr}", fill=True, ln=True)

    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*ItineraryPDF.LIGHT_GRAY)
    pdf.multi_cell(0, 5, itinerary.get("currency_note", ""))

    # ── Emergency Contacts Page ──────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(10, 14, 26)
    pdf.rect(0, 0, 210, 297, "F")

    pdf.chapter_title("🆘 Emergency Contacts & Safety Checklist")

    # Detect country
    dest = itinerary.get("destination", "")
    country_key = "Default"
    for country in EMERGENCY_CONTACTS:
        if country.lower() in dest.lower():
            country_key = country
            break
    contacts = EMERGENCY_CONTACTS.get(country_key, EMERGENCY_CONTACTS["Default"])

    contact_items = [
        ("🚔 Police / Emergency", contacts.get("police", "112")),
        ("🚑 Ambulance", contacts.get("ambulance", "112")),
        ("🗺️ Tourist Police", contacts.get("tourist_police", "N/A")),
        ("🏛️ US Embassy", contacts.get("embassy_us", "www.usembassy.gov")),
    ]
    pdf.set_font("Helvetica", "", 10)
    for label, value in contact_items:
        pdf.set_text_color(*ItineraryPDF.ORANGE)
        pdf.cell(60, 7, label)
        pdf.set_text_color(*ItineraryPDF.WHITE)
        pdf.cell(0, 7, value, ln=True)
    pdf.ln(5)

    # Pre-travel checklist
    pdf.chapter_title("✅ Pre-Travel Checklist")
    checklist = [
        "Passport valid for 6+ months beyond travel date",
        "Travel insurance purchased and policy number noted",
        "Hotel/accommodation reservations confirmed & printed",
        "Flight/transport tickets downloaded offline",
        "Local currency exchanged or ATM plan arranged",
        "Important medications packed with prescriptions",
        "Phone unlocked or international SIM/data plan activated",
        "Emergency contacts saved in phone & written down",
        "Copies of all documents in email/cloud storage",
        "Notify bank of travel dates to avoid card blocks",
        "Download offline maps (Google Maps / Maps.me)",
        "Check visa requirements and entry conditions",
    ]
    pdf.set_font("Helvetica", "", 9)
    for item in checklist:
        pdf.set_text_color(*ItineraryPDF.LIGHT_GRAY)
        pdf.cell(8, 6, "☐")
        pdf.set_text_color(*ItineraryPDF.WHITE)
        pdf.cell(0, 6, item, ln=True)

    # ── Output ───────────────────────────────────────────────────────────────
    pdf_output = pdf.output(dest="S")
    if isinstance(pdf_output, str):
        return pdf_output.encode("latin-1")
    return bytes(pdf_output)
