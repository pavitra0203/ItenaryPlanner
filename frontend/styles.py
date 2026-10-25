"""
styles.py — Modern Minimalist (Nordic / Japandi) Design System.
Curated, high-editorial aesthetic with warm wabi-sabi paper tones,
woodcraft walnut accents, matcha sage, and terracotta highlights.
"""

def get_css() -> str:
    return """
<style>
/* ─────────────────────────────────────────────────────────────
   0. GOOGLE FONTS IMPORT
───────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

/* ─────────────────────────────────────────────────────────────
   1. GLOBAL RESET & BASE ATMOSPHERE
   Palette Tokens:
     Canvas:      #F7F5F0 (Warm Washi Paper)
     Card/White:  #FFFFFF (Ceramic)
     Elevated:    #EFEBE3 (Warm Linen / Oat)
     Border:      #E4DED4 (Muted Stone)
     Border-Soft: #EDE8DF (Hairline Tatami)
     Ink-1:       #24201D (Deep Sumi Charcoal)
     Ink-2:       #5A524A (Warm Pebble / Slate)
     Ink-3:       #9C9287 (Muted Ash)
     Walnut:      #785438 (Primary Woodcraft Accent)
     Walnut-Dark: #62422A (Deep Cedar)
     Walnut-Soft: #F7F2EC (Walnut Paper Tint)
     Matcha/Sage: #52735B (Nordic Pine / Japanese Green)
     Terracotta:  #B3653E (Warm Baked Earth)
───────────────────────────────────────────────────────────── */
*, *::before, *::after {
    box-sizing: border-box;
}

html, body,
[class*="st-"], [data-testid],
.stApp, .stApp > div,
div[data-testid="stAppViewContainer"],
div[data-testid="stAppViewBlockContainer"] {
    font-family: 'Plus Jakarta Sans', 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
}

/* Preserve Material Symbols ligature rendering */
[data-testid*="material" i],
[data-testid*="Material" i],
span[class*="material-symbols"],
span[class*="MaterialSymbols"],
span[translate="no"] {
    font-family: 'Material Symbols Rounded' !important;
    font-weight: normal !important;
    font-style: normal !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    display: inline-block !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    -webkit-font-feature-settings: 'liga' !important;
    -webkit-font-smoothing: antialiased !important;
}

/* Force Warm Paper Background */
.stApp,
div[data-testid="stAppViewContainer"],
div[data-testid="stAppViewBlockContainer"],
.main,
.main > div {
    background-color: #F7F5F0 !important;
}

/* ─────────────────────────────────────────────────────────────
   2. STREAMLIT CHROME & SIDEBAR TOGGLE BUTTONS
───────────────────────────────────────────────────────────── */
#MainMenu { visibility: hidden !important; display: none !important; }
footer    { visibility: hidden !important; display: none !important; }
[data-testid="stDecoration"]   { display: none !important; }
[data-testid="stDeployButton"],
.stDeployButton,
[data-testid="stAppDeployButton"],
button[data-testid="stAppDeployButton"],
button[data-testid="stDeployButton"],
.stAppDeployButton {
    display: none !important;
    visibility: hidden !important;
}
[data-testid="stStatusWidget"] { display: none !important; }
[data-testid="manage-app-button"] { display: none !important; }
div[data-testid="stKeyboardShortcutsModal"] { display: none !important; }
button[title*="shortcuts" i],
button[aria-label*="shortcuts" i] {
    display: none !important;
}

/* Header & Toolbar: keep transparent and allow stExpandSidebarButton to show */
header,
header[data-testid="stHeader"] {
    background-color: transparent !important;
    background: transparent !important;
    box-shadow: none !important;
    z-index: 99 !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
    visibility: visible !important;
    display: flex !important;
}

[data-testid="stToolbar"] [data-testid="stStatusWidget"],
[data-testid="stToolbar"] [data-testid="stDeployButton"],
[data-testid="stToolbar"] .stDeployButton,
[data-testid="stToolbar"] [data-testid="stAppDeployButton"],
[data-testid="stToolbar"] .stAppDeployButton,
[data-testid="stToolbar"] [data-testid="manage-app-button"],
[data-testid="stToolbar"] button[title*="menu" i],
[data-testid="stToolbar"] button[aria-label*="menu" i],
[data-testid="stToolbar"] #MainMenu {
    display: none !important;
}

/* ── Sidebar Toggle Buttons (Collapse & Expand) ── */
/* When sidebar is collapsed: expand button in top-left */
[data-testid="stExpandSidebarButton"],
button[data-testid="stExpandSidebarButton"],
[data-testid="collapsedControl"],
div[data-testid="collapsedControl"],
div[data-testid="collapsedControl"] button,
.st-emotion-cache-121gac5 {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 0.85rem !important;
    left: 0.85rem !important;
    z-index: 999999 !important;
    width: 2.5rem !important;
    height: 2.5rem !important;
    background-color: #FAF8F4 !important;
    border: 1px solid #D8D1C5 !important;
    border-radius: 8px !important;
    color: #5A524A !important;
    box-shadow: 0 2px 10px rgba(45, 38, 30, 0.08) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    cursor: pointer !important;
    pointer-events: auto !important;
    overflow: hidden !important;
}

[data-testid="stExpandSidebarButton"]:hover,
button[data-testid="stExpandSidebarButton"]:hover,
[data-testid="collapsedControl"]:hover,
div[data-testid="collapsedControl"] button:hover {
    background-color: #FFFFFF !important;
    border-color: #785438 !important;
    color: #785438 !important;
    box-shadow: 0 4px 14px rgba(45, 38, 30, 0.14) !important;
    transform: scale(1.05) !important;
}

[data-testid="stExpandSidebarButton"] span,
button[data-testid="stExpandSidebarButton"] span,
[data-testid="stExpandSidebarButton"] svg,
button[data-testid="stExpandSidebarButton"] svg,
[data-testid="collapsedControl"] svg {
    font-size: 1.35rem !important;
    color: #5A524A !important;
    fill: #5A524A !important;
    stroke: #5A524A !important;
    width: 1.35rem !important;
    height: 1.35rem !important;
}

[data-testid="stExpandSidebarButton"]:hover span,
button[data-testid="stExpandSidebarButton"]:hover span,
[data-testid="stExpandSidebarButton"]:hover svg,
button[data-testid="stExpandSidebarButton"]:hover svg,
[data-testid="collapsedControl"] button:hover svg {
    color: #785438 !important;
    fill: #785438 !important;
    stroke: #785438 !important;
}

/* When sidebar is expanded: collapse button in sidebar header */
[data-testid="stSidebarCollapseButton"],
div[data-testid="stSidebarCollapseButton"],
button[data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button,
section[data-testid="stSidebar"] button[data-testid="stBaseButton-header"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    visibility: visible !important;
    opacity: 1 !important;
    background-color: #FAF8F4 !important;
    border: 1px solid #D8D1C5 !important;
    border-radius: 6px !important;
    color: #5A524A !important;
    width: 2.2rem !important;
    height: 2.2rem !important;
    padding: 0 !important;
    box-shadow: 0 1px 3px rgba(45, 38, 30, 0.05) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    pointer-events: auto !important;
    overflow: hidden !important;
}

[data-testid="stSidebarCollapseButton"]:hover,
div[data-testid="stSidebarCollapseButton"]:hover,
button[data-testid="stSidebarCollapseButton"]:hover,
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover,
section[data-testid="stSidebar"] button[data-testid="stBaseButton-header"]:hover {
    background-color: #FFFFFF !important;
    border-color: #785438 !important;
    color: #785438 !important;
    box-shadow: 0 3px 8px rgba(45, 38, 30, 0.08) !important;
    transform: scale(1.05) !important;
}

[data-testid="stSidebarCollapseButton"] span,
button[data-testid="stSidebarCollapseButton"] span,
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button span,
[data-testid="stSidebarCollapseButton"] svg,
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] svg,
section[data-testid="stSidebar"] button[data-testid="stBaseButton-header"] svg {
    font-size: 1.25rem !important;
    color: #5A524A !important;
    fill: #5A524A !important;
    stroke: #5A524A !important;
    width: 1.2rem !important;
    height: 1.2rem !important;
}

[data-testid="stSidebarCollapseButton"]:hover span,
button[data-testid="stSidebarCollapseButton"]:hover span,
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover span,
[data-testid="stSidebarCollapseButton"]:hover svg,
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover svg,
section[data-testid="stSidebar"] button[data-testid="stBaseButton-header"]:hover svg {
    color: #785438 !important;
    fill: #785438 !important;
    stroke: #785438 !important;
}

/* ─────────────────────────────────────────────────────────────
   3. MAIN CONTENT CONTAINER
───────────────────────────────────────────────────────────── */
.main .block-container {
    padding: 2.25rem 3.5rem 6rem !important;
    max-width: 1140px !important;
    background-color: #F7F5F0 !important;
}

/* ─────────────────────────────────────────────────────────────
   4. SIDEBAR — TRANQUIL LINEN ALABASTER
───────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div:first-child {
    background-color: #FAF9F6 !important;
    border-right: 1px solid #E6E1D7 !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] * {
    color: #24201D !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #5A524A !important;
    font-size: 0.82rem !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #24201D !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
}

section[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid #E6E1D7 !important;
    margin: 1.25rem 0 !important;
}

/* ─────────────────────────────────────────────────────────────
   5. HERO HEADER — WABI-SABI HIGH EDITORIAL
───────────────────────────────────────────────────────────── */
.hero-header {
    background: #FFFFFF !important;
    border: 1px solid #E4DED4 !important;
    border-radius: 8px !important;
    padding: 2.75rem 3.25rem 2.25rem !important;
    margin-bottom: 1.5rem !important;
    text-align: center !important;
    position: relative !important;
    box-shadow: 0 4px 24px -4px rgba(45, 38, 30, 0.04), 0 1px 3px rgba(45, 38, 30, 0.02) !important;
}

.hero-header::before {
    content: '' !important;
    position: absolute !important;
    top: 0; left: 0; right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, #785438 0%, #B3653E 50%, #52735B 100%) !important;
    border-radius: 8px 8px 0 0 !important;
}

.hero-title {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 3.3rem !important;
    font-weight: 500 !important;
    color: #24201D !important;
    letter-spacing: -0.02em !important;
    line-height: 1.15 !important;
    margin-bottom: 0.4rem !important;
    background: none !important;
    -webkit-text-fill-color: #24201D !important;
}

.hero-title em {
    font-style: italic !important;
    font-weight: 400 !important;
    color: #785438 !important;
    -webkit-text-fill-color: #785438 !important;
    padding-right: 0.08em !important;
}

.hero-tagline {
    font-family: 'Plus Jakarta Sans', 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    color: #9C9287 !important;
    font-weight: 500 !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
}

.hero-badges {
    display: flex !important;
    gap: 0.5rem !important;
    justify-content: center !important;
    margin-top: 1.4rem !important;
    flex-wrap: wrap !important;
}

.hero-badge {
    background: #FAF8F4 !important;
    border: 1px solid #E4DED4 !important;
    color: #5A524A !important;
    padding: 0.28rem 0.85rem !important;
    border-radius: 20px !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: all 0.2s ease !important;
}

.hero-badge:hover {
    background: #FFFFFF !important;
    border-color: #785438 !important;
    color: #785438 !important;
}

/* Active Trip Strip */
.active-trip-strip {
    display: flex !important;
    gap: 0.5rem !important;
    flex-wrap: wrap !important;
    margin-bottom: 1.75rem !important;
    align-items: center !important;
    padding: 0.65rem 1.15rem !important;
    background: #FFFFFF !important;
    border: 1px solid #E4DED4 !important;
    border-radius: 8px !important;
    box-shadow: 0 1px 4px rgba(45, 38, 30, 0.03) !important;
}

/* ─────────────────────────────────────────────────────────────
   6. TABS NAVIGATION — ARCHITECTURAL & MINIMALIST
───────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #E2DCD2 !important;
    border-radius: 0 !important;
    padding: 0 !important;
    gap: 0.5rem !important;
    box-shadow: none !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 6px 6px 0 0 !important;
    color: #8C8276 !important;
    font-family: 'Plus Jakarta Sans', 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.75rem 1.4rem !important;
    margin-bottom: -1px !important;
    transition: all 0.2s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #24201D !important;
    background: rgba(120, 84, 56, 0.04) !important;
}

.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #785438 !important;
    border-bottom: 2.5px solid #785438 !important;
    box-shadow: none !important;
    font-weight: 600 !important;
}

.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.85rem !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ─────────────────────────────────────────────────────────────
   7. CARDS & SURFACES
───────────────────────────────────────────────────────────── */
.card {
    background: #FFFFFF !important;
    border: 1px solid #E4DED4 !important;
    border-radius: 8px !important;
    padding: 1.5rem 1.65rem !important;
    margin-bottom: 1.25rem !important;
    box-shadow: 0 2px 10px -2px rgba(45, 38, 30, 0.04), 0 1px 3px rgba(45, 38, 30, 0.02) !important;
    transition: all 0.2s ease !important;
}

.card:hover {
    box-shadow: 0 6px 20px -4px rgba(45, 38, 30, 0.07), 0 2px 5px rgba(45, 38, 30, 0.03) !important;
    border-color: #D8D1C5 !important;
}

/* ─────────────────────────────────────────────────────────────
   8. DESTINATION CARDS
───────────────────────────────────────────────────────────── */
.dest-card {
    background: #FFFFFF !important;
    border: 1px solid #E4DED4 !important;
    border-radius: 8px !important;
    padding: 1.85rem 2rem !important;
    margin-bottom: 1.25rem !important;
    transition: all 0.25s ease !important;
    position: relative !important;
    box-shadow: 0 3px 14px -3px rgba(45, 38, 30, 0.04), 0 1px 3px rgba(45, 38, 30, 0.02) !important;
}

.dest-card:hover {
    box-shadow: 0 8px 28px -4px rgba(45, 38, 30, 0.08), 0 2px 6px rgba(45, 38, 30, 0.04) !important;
    transform: translateY(-2px) !important;
    border-color: #D5CEBF !important;
}

.dest-card-city {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 1.85rem !important;
    font-weight: 600 !important;
    color: #24201D !important;
    margin-bottom: 0.15rem !important;
    letter-spacing: -0.01em !important;
    background: none !important;
    -webkit-text-fill-color: #24201D !important;
}

.dest-card-match {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.35rem !important;
    background: #EDF4EF !important;
    border: 1px solid #C6DBD0 !important;
    color: #44634D !important;
    padding: 0.2rem 0.75rem !important;
    border-radius: 20px !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.85rem !important;
}

.dest-tags {
    display: flex !important;
    gap: 0.45rem !important;
    flex-wrap: wrap !important;
    margin-bottom: 0.95rem !important;
}

.dest-tag {
    background: #FAF8F4 !important;
    border: 1px solid #E4DED4 !important;
    color: #5A524A !important;
    padding: 0.2rem 0.65rem !important;
    border-radius: 4px !important;
    font-size: 0.73rem !important;
    font-weight: 500 !important;
}

.dest-why {
    color: #5A524A !important;
    font-size: 0.92rem !important;
    line-height: 1.65 !important;
    font-style: italic !important;
    margin-bottom: 0.95rem !important;
    padding-left: 0.85rem !important;
    border-left: 2px solid #E4DED4 !important;
}

.dest-meta {
    display: flex !important;
    gap: 1.75rem !important;
    color: #9C9287 !important;
    font-size: 0.8rem !important;
    border-top: 1px solid #EFEAE2 !important;
    padding-top: 0.85rem !important;
}

/* ─────────────────────────────────────────────────────────────
   9. BUDGET TRACKER & METRICS
───────────────────────────────────────────────────────────── */
.budget-tracker {
    background: #FFFFFF !important;
    border: 1px solid #E4DED4 !important;
    border-radius: 8px !important;
    padding: 1.6rem 1.85rem !important;
    margin-bottom: 1.5rem !important;
    box-shadow: 0 2px 10px -2px rgba(45, 38, 30, 0.04) !important;
}

.budget-title {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #9C9287 !important;
    margin-bottom: 1.25rem !important;
}

.budget-bar-bg {
    background: #ECE7DF !important;
    border-radius: 50px !important;
    height: 6px !important;
    overflow: hidden !important;
    margin-bottom: 0.45rem !important;
}

.budget-bar-fill {
    height: 100% !important;
    border-radius: 50px !important;
    transition: width 0.9s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.budget-stats {
    display: flex !important;
    justify-content: space-between !important;
    font-size: 0.75rem !important;
    color: #9C9287 !important;
}

/* ─────────────────────────────────────────────────────────────
   10. ITINERARY — DAY CARDS & SLOTS (EDITORIAL JOURNAL)
───────────────────────────────────────────────────────────── */
.day-card {
    background: #FFFFFF !important;
    border: 1px solid #E4DED4 !important;
    border-radius: 8px !important;
    margin-bottom: 1.65rem !important;
    overflow: hidden !important;
    box-shadow: 0 3px 12px -3px rgba(45, 38, 30, 0.04) !important;
}

.day-header {
    background: #F7F4EE !important;
    padding: 1.15rem 1.75rem !important;
    border-bottom: 1px solid #E4DED4 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
}

.day-title {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 1.35rem !important;
    font-weight: 600 !important;
    color: #24201D !important;
    letter-spacing: -0.01em !important;
    background: none !important;
    -webkit-text-fill-color: #24201D !important;
}

.day-cluster {
    font-size: 0.68rem !important;
    color: #785438 !important;
    background: #FFFFFF !important;
    padding: 0.22rem 0.75rem !important;
    border-radius: 20px !important;
    border: 1px solid #E4DED4 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

.slot-row {
    display: grid !important;
    grid-template-columns: 135px 1fr auto !important;
    gap: 1.25rem !important;
    padding: 1.15rem 1.75rem !important;
    border-bottom: 1px solid #EFEAE2 !important;
    align-items: start !important;
    transition: background 0.18s ease !important;
}

.slot-row:hover { background: #FAF9F6 !important; }
.slot-row:last-child { border-bottom: none !important; }

.slot-time {
    font-size: 0.74rem !important;
    color: #8C8276 !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    padding-top: 0.1rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.slot-period-badge {
    display: inline-block !important;
    padding: 0.16rem 0.6rem !important;
    border-radius: 4px !important;
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    margin-top: 0.35rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Authentic Japanese-Nordic Season/Period Colors */
.period-morning {
    background: #FDF4EE !important;
    color: #B3653E !important;
    border: 1px solid #F0D5C4 !important;
}
.period-lunch {
    background: #EDF4EF !important;
    color: #44634D !important;
    border: 1px solid #C6DBD0 !important;
}
.period-afternoon {
    background: #F7F2EC !important;
    color: #785438 !important;
    border: 1px solid #DECFC1 !important;
}
.period-evening {
    background: #F2F1F8 !important;
    color: #555273 !important;
    border: 1px solid #D5D2E5 !important;
}

.slot-activity {
    font-size: 0.98rem !important;
    font-weight: 600 !important;
    color: #24201D !important;
    margin-bottom: 0.25rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.slot-desc {
    font-size: 0.84rem !important;
    color: #5A524A !important;
    line-height: 1.65 !important;
    margin-bottom: 0.4rem !important;
}

.slot-tip {
    font-size: 0.76rem !important;
    color: #8C8276 !important;
    font-style: italic !important;
    display: flex !important;
    align-items: flex-start !important;
    gap: 0.3rem !important;
}

.slot-cost { text-align: right !important; min-width: 80px !important; }
.cost-usd  { font-size: 0.96rem !important; font-weight: 700 !important; color: #44634D !important; }
.cost-inr  { font-size: 0.72rem !important; color: #9C9287 !important; }
.cost-local{ font-size: 0.72rem !important; color: #9C9287 !important; }

.day-footer {
    background: #F7F4EE !important;
    padding: 0.85rem 1.75rem !important;
    border-top: 1px solid #E4DED4 !important;
    display: flex !important;
    justify-content: flex-end !important;
    gap: 1.5rem !important;
    align-items: center !important;
}

.day-total-label {
    font-size: 0.72rem !important;
    color: #8C8276 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-weight: 500 !important;
}

.day-total-val {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #785438 !important;
}

/* ─────────────────────────────────────────────────────────────
   11. SECTION HEADERS
───────────────────────────────────────────────────────────── */
.section-header {
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
    margin-bottom: 1.5rem !important;
    padding-bottom: 0.85rem !important;
    border-bottom: 1px solid #E2DCD2 !important;
}

.section-header h2,
.section-header h3 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 1.65rem !important;
    font-weight: 600 !important;
    color: #24201D !important;
    letter-spacing: -0.01em !important;
    background: none !important;
    -webkit-text-fill-color: #24201D !important;
}

.section-icon {
    font-size: 1.1rem !important;
    color: #785438 !important;
}

/* ─────────────────────────────────────────────────────────────
   12. STATUS PILLS & BADGES
───────────────────────────────────────────────────────────── */
.status-pill {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.35rem !important;
    padding: 0.25rem 0.8rem !important;
    border-radius: 20px !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.status-demo {
    background: #FDF4EE !important;
    border: 1px solid #F0D5C4 !important;
    color: #B3653E !important;
}

.status-live {
    background: #EDF4EF !important;
    border: 1px solid #C6DBD0 !important;
    color: #44634D !important;
}

/* ─────────────────────────────────────────────────────────────
   13. TRIP HISTORY CARDS
───────────────────────────────────────────────────────────── */
.trip-hist-card {
    background: #FFFFFF !important;
    border: 1px solid #E4DED4 !important;
    border-radius: 8px !important;
    padding: 1.15rem 1.5rem !important;
    margin-bottom: 0.75rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px -2px rgba(45, 38, 30, 0.03) !important;
}

.trip-hist-card:hover {
    box-shadow: 0 5px 16px -3px rgba(45, 38, 30, 0.07) !important;
    border-color: #D5CEBF !important;
    transform: translateY(-1px) !important;
}

.trip-hist-dest {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: #24201D !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
}

.trip-hist-meta {
    font-size: 0.78rem !important;
    color: #8C8276 !important;
    margin-top: 0.15rem !important;
}

.trip-hist-badge {
    background: #F7F4EE !important;
    border: 1px solid #E4DED4 !important;
    color: #785438 !important;
    padding: 0.25rem 0.75rem !important;
    border-radius: 20px !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
}

/* ─────────────────────────────────────────────────────────────
   14. STREAMLIT NATIVE WIDGET OVERRIDES — REFINED WOOD & STONE
───────────────────────────────────────────────────────────── */

/* ── Primary & Action Buttons (WARM WALNUT & NATURAL CEDAR) ── */
div[data-testid="stButton"] button,
.stButton button,
button[data-testid="baseButton-secondary"],
button[data-testid="baseButton-primary"],
button[kind="primary"] {
    background-color: #6E4B30 !important;
    color: #FAF8F5 !important;
    border: 1px solid #6E4B30 !important;
    border-radius: 6px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.55rem 1.45rem !important;
    box-shadow: 0 2px 6px rgba(110, 75, 48, 0.14) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
}

div[data-testid="stButton"] button p,
.stButton button p,
button[data-testid="baseButton-secondary"] p,
button[data-testid="baseButton-primary"] p {
    color: #FAF8F5 !important;
    font-weight: 500 !important;
}

div[data-testid="stButton"] button:hover,
.stButton button:hover,
button[data-testid="baseButton-secondary"]:hover,
button[data-testid="baseButton-primary"]:hover,
button[kind="primary"]:hover {
    background-color: #845B3B !important;
    border-color: #845B3B !important;
    color: #FFFFFF !important;
    box-shadow: 0 5px 14px rgba(110, 75, 48, 0.22) !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stButton"] button:hover p,
.stButton button:hover p,
button[data-testid="baseButton-secondary"]:hover p,
button[data-testid="baseButton-primary"]:hover p {
    color: #FFFFFF !important;
}

div[data-testid="stButton"] button:active,
.stButton button:active,
button[data-testid="baseButton-secondary"]:active,
button[data-testid="baseButton-primary"]:active {
    background-color: #5A3C24 !important;
    border-color: #5A3C24 !important;
    transform: translateY(0) !important;
    box-shadow: 0 2px 4px rgba(110, 75, 48, 0.15) !important;
}

/* Sidebar Secondary / Outline Button (e.g. Reset Everything) */
section[data-testid="stSidebar"] div[data-testid="stButton"] button,
section[data-testid="stSidebar"] .stButton button,
section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
    background-color: #FAF8F4 !important;
    color: #5A524A !important;
    border: 1px solid #D8D1C5 !important;
    box-shadow: 0 1px 3px rgba(45, 38, 30, 0.03) !important;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] button p,
section[data-testid="stSidebar"] .stButton button p {
    color: #5A524A !important;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover,
section[data-testid="stSidebar"] .stButton button:hover,
section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover {
    background-color: #FFFFFF !important;
    border-color: #785438 !important;
    color: #785438 !important;
    box-shadow: 0 3px 8px rgba(45, 38, 30, 0.06) !important;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover p,
section[data-testid="stSidebar"] .stButton button:hover p {
    color: #785438 !important;
}

/* Download Button (Nordic Pine Matcha) */
.stDownloadButton > button {
    background-color: #4E6B56 !important;
    color: #FFFFFF !important;
    border: 1px solid #4E6B56 !important;
    border-radius: 6px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 2px 6px rgba(78, 107, 86, 0.15) !important;
    transition: all 0.2s ease !important;
}

.stDownloadButton > button:hover {
    background-color: #5D8067 !important;
    border-color: #5D8067 !important;
    color: #FFFFFF !important;
    box-shadow: 0 5px 14px rgba(78, 107, 86, 0.24) !important;
    transform: translateY(-1px) !important;
}

/* ── Text Inputs, Number Inputs, TextAreas ── */
.stTextInput > div > div,
div[data-testid="stTextInputRootElement"],
.stNumberInput > div > div,
.stTextArea > div > div {
    background-color: #FFFFFF !important;
    border: 1px solid #D8D1C5 !important;
    border-radius: 6px !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

.stTextInput > div > div:focus-within,
div[data-testid="stTextInputRootElement"]:focus-within,
.stNumberInput > div > div:focus-within,
.stTextArea > div > div:focus-within {
    border-color: #785438 !important;
    box-shadow: 0 0 0 3px rgba(120, 84, 56, 0.12) !important;
}

.stTextInput input,
div[data-testid="stTextInputRootElement"] input,
.stNumberInput input,
.stTextArea textarea {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    color: #24201D !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.875rem !important;
}

/* Hide intrusive 'Press Enter to apply' overlay pill */
[data-testid="InputInstructions"],
div[data-testid="InputInstructions"],
.stInputInstructions,
div[class*="InputInstructions"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Stepper buttons in number inputs */
.stNumberInput button {
    background-color: #FAF8F4 !important;
    border: 1px solid #D8D1C5 !important;
    color: #5A524A !important;
    border-radius: 4px !important;
}
.stNumberInput button:hover {
    background-color: #EDE8DF !important;
    color: #785438 !important;
}

/* Placeholder */
input::placeholder, textarea::placeholder {
    color: #B5ACA1 !important;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div > div {
    background-color: #FFFFFF !important;
    border-color: #D8D1C5 !important;
    border-radius: 6px !important;
    color: #24201D !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

div[data-baseweb="select"] svg {
    fill: #8C8276 !important;
}

div[data-baseweb="popover"] ul[role="listbox"],
div[data-baseweb="popover"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E4DED4 !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 28px rgba(45, 38, 30, 0.1) !important;
}

div[data-baseweb="popover"] li {
    color: #24201D !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.875rem !important;
    background: transparent !important;
    padding: 0.6rem 1rem !important;
}

div[data-baseweb="popover"] li:hover {
    background-color: #F7F4EE !important;
    color: #785438 !important;
}

div[data-baseweb="popover"] li[aria-selected="true"] {
    background-color: #F3ECE2 !important;
    color: #785438 !important;
    font-weight: 600 !important;
}

/* ── Multiselect Tags (FIX CRITICAL CONTRAST & STYLING) ── */
[data-tag],
div[data-tag],
span[data-tag],
[data-baseweb="tag"],
div[data-baseweb="tag"],
span[data-baseweb="tag"],
.stMultiSelect [data-tag],
.stMultiSelect [data-baseweb="tag"],
div[data-testid="stMultiSelectTagsContainer"] [data-tag] {
    background-color: #EDE8DF !important;
    border: 1px solid #D8D1C5 !important;
    border-radius: 5px !important;
    padding: 0.2rem 0.55rem !important;
    margin: 2px 3px 2px 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    box-shadow: 0 1px 2px rgba(45, 38, 30, 0.04) !important;
}

[data-tag] *,
div[data-tag] *,
span[data-tag] *,
[data-baseweb="tag"] *,
div[data-baseweb="tag"] *,
span[data-baseweb="tag"] *,
.stMultiSelect [data-tag] *,
.stMultiSelect [data-baseweb="tag"] *,
div[data-testid="stMultiSelectTagsContainer"] [data-tag] * {
    color: #24201D !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
}

[data-tag] button,
[data-tag] [role="button"],
.stMultiSelect [data-tag] button,
.stMultiSelect [data-baseweb="tag"] [role="button"] {
    background: transparent !important;
    border: none !important;
    cursor: pointer !important;
    padding: 0 !important;
    margin-left: 0.35rem !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    opacity: 0.75 !important;
}

[data-tag] button:hover,
[data-tag] [role="button"]:hover,
.stMultiSelect [data-tag] button:hover {
    opacity: 1 !important;
}

[data-tag] svg,
[data-tag] button svg,
[data-baseweb="tag"] svg,
.stMultiSelect [data-tag] svg {
    color: #785438 !important;
    fill: #785438 !important;
    stroke: #785438 !important;
    width: 0.8rem !important;
    height: 0.8rem !important;
}

/* ── Expander ── */
details,
[data-testid="stExpander"] details {
    border: 1px solid #E4DED4 !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    background: #FFFFFF !important;
    margin-bottom: 0.75rem !important;
    box-shadow: 0 1px 4px rgba(45, 38, 30, 0.02) !important;
}

[data-testid="stExpander"] summary,
details summary {
    background-color: #FAF8F4 !important;
    color: #24201D !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 0.8rem 1.15rem !important;
    border-radius: 0 !important;
    list-style: none !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: background 0.18s ease !important;
}

[data-testid="stExpander"] summary:hover,
details summary:hover {
    background-color: #F3ECE2 !important;
}

[data-testid="stExpander"] summary svg {
    color: #8C8276 !important;
    fill: #8C8276 !important;
}

/* ── Alerts & Notifications ── */
div[data-testid="stNotification"],
.stAlert, .stInfo, .stSuccess, .stWarning, .stError {
    border-radius: 8px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.875rem !important;
    border-width: 1px !important;
    border-style: solid !important;
    box-shadow: 0 2px 8px rgba(45, 38, 30, 0.03) !important;
}

.stInfo, div[data-testid="stNotification"][data-type="info"] {
    background-color: #FAF8F4 !important;
    border-color: #E2DCD2 !important;
    color: #4A423A !important;
}

.stSuccess, div[data-testid="stNotification"][data-type="success"] {
    background-color: #EDF4EF !important;
    border-color: #C6DBD0 !important;
    color: #35533D !important;
}

.stWarning, div[data-testid="stNotification"][data-type="warning"] {
    background-color: #FDF4EE !important;
    border-color: #F0D5C4 !important;
    color: #8C4F2C !important;
}

.stError, div[data-testid="stNotification"][data-type="error"] {
    background-color: #FDF2F0 !important;
    border-color: #ECCDC8 !important;
    color: #8A3428 !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #FFFFFF !important;
    border: 1px solid #E4DED4 !important;
    border-radius: 8px !important;
    padding: 1.15rem 1.35rem !important;
    box-shadow: 0 1px 4px rgba(45, 38, 30, 0.02) !important;
}

[data-testid="stMetricValue"],
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 1.85rem !important;
    font-weight: 600 !important;
    color: #785438 !important;
    background: none !important;
    -webkit-text-fill-color: #785438 !important;
}

[data-testid="stMetricLabel"],
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #8C8276 !important;
}

[data-testid="stMetricDelta"] {
    color: #44634D !important;
}

/* ── Slider ── */
.stSlider [data-testid="stSlider"] > div > div {
    color: #785438 !important;
}

.stSlider div[role="slider"] {
    background-color: #785438 !important;
    border-color: #785438 !important;
}

.stSlider [data-baseweb="slider"] div[role="progressbar"] {
    background-color: #785438 !important;
}

/* ── Checkboxes & Radios ── */
.stCheckbox label,
.stRadio label,
.stRadio [data-testid="stMarkdownContainer"] p {
    color: #5A524A !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stCheckbox input[type="checkbox"],
.stRadio input[type="radio"] {
    accent-color: #785438 !important;
}

/* ── Widget Labels ── */
label[data-testid="stWidgetLabel"],
.stTextInput label,
.stSelectbox label,
.stNumberInput label,
.stMultiSelect label,
.stTextArea label,
.stSlider label,
.stDateInput label,
.stRadio label:first-child,
.stCheckbox label {
    color: #5A524A !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Typography & Markdown ── */
.stMarkdown p, .stMarkdown li {
    color: #5A524A !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important;
    line-height: 1.65 !important;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #24201D !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    background: none !important;
    -webkit-text-fill-color: #24201D !important;
}

.stMarkdown strong { color: #24201D !important; }
.stMarkdown a { color: #785438 !important; text-decoration: underline !important; }

.stCaption, [data-testid="stCaptionContainer"] {
    color: #9C9287 !important;
    font-size: 0.76rem !important;
}

[data-testid="stSpinner"] > div {
    border-top-color: #785438 !important;
}

/* ─────────────────────────────────────────────────────────────
   15. CUSTOM SCROLLBAR
───────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F7F5F0; }
::-webkit-scrollbar-thumb { background: #D5CEBF; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #785438; }

/* ─────────────────────────────────────────────────────────────
   16. DELICATE ENTRANCE ANIMATION
───────────────────────────────────────────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeInUp 0.35s ease forwards; }
</style>
"""
