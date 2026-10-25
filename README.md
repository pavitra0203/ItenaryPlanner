# ✈️ Personalized Travel Itinerary Planner
### Skill Wallet Capstone Project 4 — Senior Travel SaaS Architecture

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.44+-FF4B4B.svg)](https://streamlit.io/)
[![Design](https://img.shields.io/badge/Design-Nordic%20%2F%20Japandi-785438.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

A production-ready, AI-orchestrated travel planning application crafted in Python with **Streamlit** and an editorial **Modern Minimalist (Nordic / Japandi)** design system.

---

## 🌿 Nordic / Japandi Design Aesthetic

The application is styled with a bespoke design system built on wabi-sabi principles, high-contrast typography, and organic tactile surfaces:

- **Warm Washi Paper Canvas** (`#F7F5F0`) & **Ceramic White Cards** (`#FFFFFF`)
- **Editorial Typography**: *Cormorant Garamond* (display serif) paired with *Plus Jakarta Sans* & *DM Sans*
- **Natural Accents**: Warm Walnut Woodcraft (`#785438`), Matcha Sage (`#52735B`), and Terracotta (`#B3653E`)
- **Interactive Collapsible Sidebar**: Dedicated floating toggle button (`»`) when collapsed, and header collapse button (`«`) with smooth transitions
- **Accessibility & Contrast**: WCAG AAA compliant text contrast, tactile inputs, and custom tag chips

---

## ✨ Core Modules & Architecture

| Module | Tab / Screen | Architectural Capability |
|---|---|---|
| 🧭 **Preferences Engine** | Sidebar | Destination (or open vibe), Duration (1–14 days), Dates, Budget Level, Travel Party, Pace, and Interests (up to 5 tags). |
| 📍 **Smart Destination Recommender** | Tab 1 | Recommends top 3 curated destinations with match confidence score, highlights, best season, and 1-click itinerary planning. |
| 🗓️ **Geo-Clustered Itinerary Generator** | Tab 2 | Sequential time-blocked day plans (Morning, Afternoon, Evening), geo-clustered sightseeing, daily budget breakdowns, and cost trackers. |
| 🎨 **Vibe Customization & Live Swaps** | Tab 3 | Fine-tune individual activity slots (swap for Adventure, Chill, Foodie, or Cultural) without regenerating the entire itinerary. |
| 💼 **Trip Management & PDF Export** | Tab 4 | Save and load trips from local persistence (`trip_db.py`), view summary metrics, and export branded offline PDFs via `fpdf2`. |

---

## 🤖 Dual AI Engine + Demo Mode

The platform supports plug-and-play AI backends with automatic failover and demo capability:

1. **Demo Mode (Default)**: Fully functional out of the box with zero API keys required. Uses rich deterministic templates.
2. **Google Gemini**: Powered by `gemini-1.5-flash` for rich, nuanced, multimodal travel advice.
3. **Groq**: Ultra-fast inference with `llama-3.3-70b-versatile` / `llama3-70b-8192`.

---

## 🚀 Quick Start

### 1. Clone & Set Up Virtual Environment

```bash
# Navigate to project directory
cd ItenaryPlanner

# Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install watchdog  # Recommended for instant hot-reload during development
```

### 3. Launch the Application

```bash
streamlit run app.py
```

The app will start at `http://localhost:8501`.

---

## 🔑 Configuration & API Keys

API keys can be supplied directly in the sidebar **API Configuration** drawer or through environment variables / `.env`:

```env
# Optional environment variables
GEMINI_API_KEY="your-gemini-api-key"
GROQ_API_KEY="your-groq-api-key"
```

- **Google Gemini Key**: [Google AI Studio](https://aistudio.google.com/)
- **Groq Key**: [Groq Cloud Console](https://console.groq.com/)

---

## 📁 Repository Structure

```
ItenaryPlanner/
├── app.py                      # Main Streamlit orchestrator & entry point
├── requirements.txt            # Python dependencies
├── trip_history.json           # Local JSON trip persistence storage
├── .streamlit/
│   └── config.toml             # Streamlit server and theme configuration
├── frontend/                   # UI Presentation Layer
│   ├── __init__.py
│   ├── styles.py               # Nordic / Japandi CSS design system & tokens
│   └── tabs/                   # Streamlit View Tabs
│       ├── __init__.py
│       ├── tab1_destinations.py# Tab 1: Smart Destination Recommender
│       ├── tab2_itinerary.py   # Tab 2: Day-by-Day Geo-Clustered Generator
│       ├── tab3_vibe.py        # Tab 3: Vibe Swapping & Slot Fine-Tuning
│       └── tab4_management.py  # Tab 4: Trip Management & PDF Export
└── backend/                    # Core Business & Service Layer
    ├── __init__.py
    ├── config.py               # Constants, vibes, party types, and seed data
    ├── ai_client.py            # Unified LLM dispatcher (Gemini, Groq, Demo)
    ├── trip_db.py              # Local persistence engine for trip history
    └── pdf_export.py           # FPDF2-based offline PDF itinerary generator
```

---

## 🛠️ Technology Stack

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/) (v1.44+)
- **Styling**: Handcrafted CSS Design System (Custom Google Fonts, CSS Grid/Flexbox, Custom Animations)
- **AI / LLMs**: Google Gemini API (`google-genai`), Groq API (`groq`)
- **Document Generation**: `fpdf2` (zero external binary dependencies)
- **Data Persistence**: JSON-backed local storage engine (`saved_trips.json`)
- **Live File Watching**: `watchdog`

---

## 🚢 Deployment

### Streamlit Community Cloud

1. Push your repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io) and log in.
3. Select this repository and set `app.py` as the main file path.
4. Add any optional secrets (`GEMINI_API_KEY`, `GROQ_API_KEY`) under **Settings → Secrets**.
5. Click **Deploy**. The app runs in Demo Mode even without secrets configured.

---

## 👨‍💻 Author — Pavitra Singh

*Built as Skill Wallet Capstone Project 4 — Senior Travel SaaS Architecture.*
