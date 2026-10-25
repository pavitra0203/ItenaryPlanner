"""
config.py - Application-wide constants and configuration settings.
"""

APP_NAME = "Personalized Travel Itinerary Planner"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Plan smarter. Travel deeper. Experience more."

# ── Demo-mode pre-canned responses (no API key needed) ──────────────────────
DEMO_DESTINATIONS = [
    {
        "city": "Lisbon, Portugal",
        "country": "Portugal",
        "match_score": 97,
        "tags": ["🌊 Coastal", "🏛️ Cultural", "🍷 Foodie", "☀️ Sunny"],
        "why": "Lisbon blends pastel-hued trams, world-class seafood, and dramatic Atlantic views—perfect for your vibe.",
        "best_time": "Apr – Jun, Sep – Oct",
        "avg_budget_usd": 120,
    },
    {
        "city": "Chiang Mai, Thailand",
        "country": "Thailand",
        "match_score": 93,
        "tags": ["🏔️ Mountains", "🛕 Temples", "🌿 Nature", "💰 Budget-Friendly"],
        "why": "Ancient temples, lush jungles, and a thriving night-market scene make Chiang Mai a backpacker's paradise.",
        "best_time": "Nov – Feb",
        "avg_budget_usd": 60,
    },
    {
        "city": "Medellín, Colombia",
        "country": "Colombia",
        "match_score": 89,
        "tags": ["🌆 Urban", "🎶 Nightlife", "🌸 Spring Climate", "🎨 Art"],
        "why": "The 'City of Eternal Spring' offers cable-car mountains, salsa nights, and cutting-edge street art.",
        "best_time": "Dec – Mar",
        "avg_budget_usd": 80,
    },
]

DEMO_ITINERARY = {
    "destination": "Lisbon, Portugal",
    "duration": 3,
    "days": [
        {
            "day": 1,
            "theme": "Historic Heart & Waterfront",
            "cluster_area": "Alfama & Baixa",
            "slots": [
                {
                    "time": "09:00 – 12:00",
                    "period": "Morning",
                    "emoji": "🌅",
                    "activity": "Explore Alfama & São Jorge Castle",
                    "description": "Wander the oldest neighborhood in Lisbon. Visit the Moorish castle for panoramic views over the city and the Tagus River.",
                    "cost_usd": 15,
                    "cost_inr": 1250,
                    "cost_local": "€12",
                    "tips": "Go early to beat crowds. Wear comfortable shoes—cobblestone streets are steep.",
                },
                {
                    "time": "12:30 – 14:00",
                    "period": "Lunch",
                    "emoji": "🍽️",
                    "activity": "Taberna da Rua das Flores",
                    "description": "Authentic petiscos (Portuguese tapas) in a charming tile-lined tavern near Chiado.",
                    "cost_usd": 22,
                    "cost_inr": 1835,
                    "cost_local": "€18",
                    "tips": "Try the bacalhau à brás (salted cod) and a glass of vinho verde.",
                },
                {
                    "time": "14:30 – 17:30",
                    "period": "Afternoon",
                    "emoji": "🚋",
                    "activity": "Ride Tram 28 & Miradouro da Graça",
                    "description": "Take the iconic yellow tram through winding streets, then walk to Graça viewpoint for golden-hour photos.",
                    "cost_usd": 5,
                    "cost_inr": 415,
                    "cost_local": "€4",
                    "tips": "Board at Martim Moniz to grab a seat before the crowd.",
                },
                {
                    "time": "19:00 – 22:00",
                    "period": "Evening",
                    "emoji": "🎶",
                    "activity": "Fado Dinner at Clube de Fado",
                    "description": "Indulge in a traditional Fado music dinner experience in the heart of Alfama. Reservations essential.",
                    "cost_usd": 55,
                    "cost_inr": 4580,
                    "cost_local": "€45",
                    "tips": "Book at least 2 days in advance. Dress smart-casual.",
                },
            ],
            "day_total_usd": 97,
            "day_total_inr": 8080,
        },
        {
            "day": 2,
            "theme": "Ocean Views & Pastéis de Nata",
            "cluster_area": "Belém & LX Factory",
            "slots": [
                {
                    "time": "09:00 – 11:30",
                    "period": "Morning",
                    "emoji": "🗼",
                    "activity": "Belém Tower & Jerónimos Monastery",
                    "description": "UNESCO World Heritage marvels on the Tagus. The Manueline monastery is one of Europe's finest Gothic buildings.",
                    "cost_usd": 18,
                    "cost_inr": 1500,
                    "cost_local": "€14",
                    "tips": "The monastery is closed on Mondays. Combo tickets save money.",
                },
                {
                    "time": "12:00 – 12:30",
                    "period": "Lunch Snack",
                    "emoji": "🥐",
                    "activity": "Pastéis de Belém – Original Custard Tarts",
                    "description": "The birthplace of the famous pastel de nata. Order 3–4 with cinnamon and powdered sugar. Pure bliss.",
                    "cost_usd": 5,
                    "cost_inr": 415,
                    "cost_local": "€4",
                    "tips": "The queue moves fast. Eat them warm at the marble counter inside.",
                },
                {
                    "time": "13:00 – 16:00",
                    "period": "Afternoon",
                    "emoji": "🛍️",
                    "activity": "LX Factory – Creative Market",
                    "description": "A repurposed industrial complex with boutique shops, street art, local designers, and amazing food stalls.",
                    "cost_usd": 25,
                    "cost_inr": 2085,
                    "cost_local": "€20",
                    "tips": "Sunday markets are the most vibrant. Budget extra for shopping.",
                },
                {
                    "time": "18:30 – 21:30",
                    "period": "Evening",
                    "emoji": "🌊",
                    "activity": "Sunset Cocktails at Park Bar + Pink Street",
                    "description": "Rooftop bar above a car park with 360° city views. Follow with nightlife along the Cais do Sodré Pink Street.",
                    "cost_usd": 30,
                    "cost_inr": 2500,
                    "cost_local": "€25",
                    "tips": "Park Bar is free entry. Arrive by 6 PM for the best sunset spot.",
                },
            ],
            "day_total_usd": 78,
            "day_total_inr": 6500,
        },
        {
            "day": 3,
            "theme": "Day Trip to Sintra Palaces",
            "cluster_area": "Sintra (40 min from Lisbon)",
            "slots": [
                {
                    "time": "08:30 – 10:00",
                    "period": "Morning Transit",
                    "emoji": "🚂",
                    "activity": "Train to Sintra",
                    "description": "Hop on the scenic train from Rossio Station. The 40-minute ride through forested hills is beautiful.",
                    "cost_usd": 6,
                    "cost_inr": 500,
                    "cost_local": "€4.60",
                    "tips": "Buy a return ticket. First train at 6:25 AM—go early!",
                },
                {
                    "time": "10:00 – 13:00",
                    "period": "Morning",
                    "emoji": "🏰",
                    "activity": "Pena Palace & Castle of the Moors",
                    "description": "Fairytale Romanticist palace perched above the clouds. The Moors' Castle offers dramatic Atlantic panoramas.",
                    "cost_usd": 25,
                    "cost_inr": 2085,
                    "cost_local": "€20",
                    "tips": "Buy combined tickets online. Wear layers—hilltop is cooler.",
                },
                {
                    "time": "13:30 – 15:00",
                    "period": "Lunch",
                    "emoji": "🍕",
                    "activity": "Café Saudade in Sintra Village",
                    "description": "Cozy café in the historic center. Try travesseiros (puff pastry with almond cream) and queijadas de Sintra.",
                    "cost_usd": 18,
                    "cost_inr": 1500,
                    "cost_local": "€14",
                    "tips": "Sintra village is walkable from the palace bus stop.",
                },
                {
                    "time": "15:30 – 18:00",
                    "period": "Afternoon",
                    "emoji": "🌿",
                    "activity": "Quinta da Regaleira & Gardens",
                    "description": "A mystical estate with neo-Gothic towers, secret tunnels, and an inverted tower descending into the earth.",
                    "cost_usd": 12,
                    "cost_inr": 1000,
                    "cost_local": "€10",
                    "tips": "The initiation well is the highlight—bring a flashlight app.",
                },
            ],
            "day_total_usd": 61,
            "day_total_inr": 5085,
        },
    ],
    "total_cost_usd": 236,
    "total_cost_inr": 19665,
    "currency_note": "Costs are estimates. Local currency: Euro (€). Exchange rate: 1 USD ≈ €0.82 ≈ ₹83.5",
}

# ── Interest & Vibe Options ──────────────────────────────────────────────────
INTERESTS = ["Food & Cuisine", "Adventure & Outdoors", "History & Culture",
             "Nightlife & Entertainment", "Art & Architecture", "Shopping",
             "Wellness & Spa", "Wildlife & Nature", "Photography", "Sports"]

VIBES = ["🏖️ Beach & Coast", "🏔️ Mountains & Trekking", "🏛️ Cultural & Historical",
         "🌆 Urban & Cosmopolitan", "🌿 Nature & Wildlife", "🎭 Arts & Festivals"]

BUDGET_LEVELS = ["💰 Budget (< $50/day)", "💳 Moderate ($50–150/day)", "💎 Luxury ($150+/day)"]
TRAVEL_PARTY = ["🧍 Solo", "👫 Couple", "👨‍👩‍👧 Family", "👯 Friends Group"]
PACE_OPTIONS = ["🛋️ Relaxed", "🚶 Moderate", "🏃 Fast-Paced"]

# ── Emergency Contact Templates ──────────────────────────────────────────────
EMERGENCY_CONTACTS = {
    "Portugal": {"police": "112", "ambulance": "112", "tourist_police": "+351 21 342 1634", "embassy_us": "+351 21 727 3300"},
    "Thailand": {"police": "191", "ambulance": "1669", "tourist_police": "1155", "embassy_us": "+66 2 205 4000"},
    "Colombia": {"police": "123", "ambulance": "125", "tourist_police": "156", "embassy_us": "+57 1 275 2000"},
    "Default": {"police": "112 / 911", "ambulance": "112 / 911", "tourist_police": "Contact local tourism office", "embassy_us": "www.usembassy.gov"},
}
