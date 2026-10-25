"""
ai_client.py - Unified AI client supporting Gemini, Groq, and demo mode.
"""

import json
import re
import streamlit as st

# ── Provider helpers ─────────────────────────────────────────────────────────

def _call_gemini(prompt: str, api_key: str) -> str:
    """Call Google Gemini with resilient model fallback and direct REST/SDK dispatch."""
    candidate_models = [
        "gemini-3.5-flash",
        "gemini-3.8-flash",
        "gemini-flash-latest",
        "gemini-2.5-flash",
        "gemini-1.5-flash",
    ]

    # Primary: Fast, direct REST API (immune to gRPC DNS/version conflicts)
    import requests
    for model_name in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            resp = requests.post(
                url,
                json={"contents": [{"parts": [{"text": prompt}]}]},
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            if resp.status_code in (404, 503):
                continue
        except Exception:
            continue

    # Secondary: SDK fallback
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        for model_name in candidate_models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                if any(err in str(e).lower() for err in ["404", "not found", "no longer available"]):
                    continue
                raise e
    except Exception as exc:
        raise exc

    raise RuntimeError("None of the supported Gemini models responded successfully. Please verify your API key.")

def _call_groq(prompt: str, api_key: str) -> str:
    """Call Groq (llama3-70b-8192) and return raw text."""
    from groq import Groq
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=4096,
    )
    return completion.choices[0].message.content

import os

def get_active_api_key(provider: str) -> str:
    """Retrieve API key from session state, st.secrets, or environment variables."""
    key = st.session_state.get("api_key", "").strip()
    placeholder_keys = {"your_gemini_api_key_here", "your_groq_api_key_here", ""}
    if key and key not in placeholder_keys:
        return key

    secret_name = "GEMINI_API_KEY" if provider == "gemini" else "GROQ_API_KEY"
    try:
        val = str(st.secrets.get(secret_name, "")).strip()
        if val and val not in placeholder_keys:
            return val
    except Exception:
        pass

    env_val = os.getenv(secret_name, "").strip()
    if env_val and env_val not in placeholder_keys:
        return env_val

    return ""


# ── Main dispatch ─────────────────────────────────────────────────────────────

def call_ai(prompt: str) -> str:
    """
    Dispatch to the active AI provider based on session state or secrets.
    Falls back to demo mode if no key is configured.
    """
    provider = st.session_state.get("ai_provider", "demo")
    api_key = get_active_api_key(provider)

    if provider == "demo" or not api_key:
        return "__DEMO__"

    try:
        if provider == "gemini":
            return _call_gemini(prompt, api_key)
        elif provider == "groq":
            return _call_groq(prompt, api_key)
        else:
            return "__DEMO__"
    except Exception as exc:
        st.error(f"⚠️ AI API error: {exc}")
        return "__DEMO__"


def extract_json(text: str) -> dict | list | None:
    """Extract the first JSON object or array from an AI response string."""
    # Try full parse first
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    # Try to find JSON block with regex
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    # Try to find bare { } or [ ]
    match = re.search(r"(\{[\s\S]+\}|\[[\s\S]+\])", text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    return None


# ── Prompt builders ───────────────────────────────────────────────────────────

def build_destination_prompt(prefs: dict) -> str:
    return f"""
You are a world-class travel expert. Based on the traveler profile below, recommend exactly 3 destinations.

Traveler Profile:
- Vibe / Mood: {prefs.get('vibe', 'Any')}
- Budget Level: {prefs.get('budget', 'Moderate')}
- Travel Dates: {prefs.get('dates', 'Flexible')}
- Party: {prefs.get('party', 'Solo')}
- Interests: {', '.join(prefs.get('interests', ['Culture']))}
- Pace: {prefs.get('pace', 'Moderate')}

Return ONLY a JSON array of exactly 3 objects with these fields:
- city (string)
- country (string)
- match_score (integer 0-100)
- tags (array of 3-4 emoji+text strings)
- why (string, 1-2 sentences explaining why this matches the traveler)
- best_time (string e.g. "Apr – Jun")
- avg_budget_usd (integer, daily budget in USD)

Return valid JSON only, no markdown, no explanation.
"""


def build_itinerary_prompt(prefs: dict) -> str:
    duration = prefs.get("duration", 3)
    return f"""
You are a master travel planner specializing in geo-clustered, time-optimized itineraries.

Trip Details:
- Destination: {prefs.get('destination', 'Paris, France')}
- Duration: {duration} days
- Budget: {prefs.get('budget', 'Moderate')}
- Party: {prefs.get('party', 'Solo')}
- Interests: {', '.join(prefs.get('interests', ['Culture', 'Food']))}
- Pace: {prefs.get('pace', 'Moderate')}
- Travel Dates: {prefs.get('dates', 'Flexible')}

CRITICAL RULES:
1. Group geographically nearby attractions on the SAME day to minimize transit time.
2. Each day must have exactly 4 slots: Morning, Lunch, Afternoon, Evening.
3. Provide realistic estimated costs in USD, INR, and local currency.
4. Include a practical insider tip for each slot.

Return ONLY a valid JSON object with this exact structure:
{{
  "destination": "City, Country",
  "duration": {duration},
  "days": [
    {{
      "day": 1,
      "theme": "Theme Name",
      "cluster_area": "Neighborhood/Area Name",
      "slots": [
        {{
          "time": "09:00 – 12:00",
          "period": "Morning",
          "emoji": "🌅",
          "activity": "Activity Name",
          "description": "2-3 sentence description",
          "cost_usd": 20,
          "cost_inr": 1670,
          "cost_local": "€16",
          "tips": "Insider tip here"
        }}
      ],
      "day_total_usd": 100,
      "day_total_inr": 8350
    }}
  ],
  "total_cost_usd": 300,
  "total_cost_inr": 25050,
  "currency_note": "Exchange rate note"
}}

Generate all {duration} days. Return valid JSON only.
"""


def build_swap_prompt(prefs: dict, day: int, slot_period: str, swap_request: str) -> str:
    destination = prefs.get("destination", "the destination")
    return f"""
You are a travel concierge. A traveler visiting {destination} wants to swap a specific activity.

Current Day: Day {day}
Slot to Replace: {slot_period}
Swap Request: "{swap_request}"
Budget Level: {prefs.get('budget', 'Moderate')}
Interests: {', '.join(prefs.get('interests', ['Culture']))}

Provide ONE replacement activity as a JSON object:
{{
  "time": "HH:MM – HH:MM",
  "period": "{slot_period}",
  "emoji": "🎯",
  "activity": "New Activity Name",
  "description": "2-3 sentence description",
  "cost_usd": 25,
  "cost_inr": 2085,
  "cost_local": "Local currency amount",
  "tips": "Insider tip"
}}

Return valid JSON only.
"""
