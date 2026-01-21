import os
from dotenv import load_dotenv

load_dotenv()

# --- API Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL_NAME = "llama-3.3-70b-versatile"

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

# --- Caching & Retries ---
CACHE_NAME = ".cache"
CACHE_EXPIRE_AFTER = 3600  # Seconds
RETRY_COUNT = 5
RETRY_BACKOFF = 0.2

# --- Tooling Configuration ---
FUZZY_MATCH_THRESHOLD = 40  # Percent

# --- Data Fetching Parameters ---
HOURLY_VARIABLES = [
    "temperature_2m", "precipitation_probability", "rain",
    "snowfall", "weather_code", "wind_speed_10m"
]

DAILY_VARIABLES = [
    "weather_code", "temperature_2m_max", "temperature_2m_min",
    "rain_sum", "snowfall_sum", "wind_speed_10m_max"
]

# --- Business Logic: WMO Weather Codes ---
WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers", 85: "Slight snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

# --- Business Logic: Historical Search Configuration ---
SEARCH_CONFIG = {
    "snow": {"col": "snowfall_sum", "op": ">", "val": 0.0, "desc": "snowfall", "unit": "cm"},
    "rain": {"col": "rain_sum", "op": ">", "val": 1.0, "desc": "noticeable rain", "unit": "mm"},
    "wind": {"col": "wind_speed_10m_max", "op": ">", "val": 50.0, "desc": "strong wind", "unit": "km/h"},
    "heat": {"col": "temperature_2m_max", "op": ">", "val": 30.0, "desc": "heatwave", "unit": "°C"},
    "frost": {"col": "temperature_2m_min", "op": "<", "val": -10.0, "desc": "severe frost", "unit": "°C"},
    "hail": {"col": "weather_code", "op": "in", "val": [96, 99], "desc": "hail / hail storm", "unit": "(WMO Code)"}
}

# --- Business Logic: Record Search Configuration ---
RECORD_CONFIG = {
    "min_temp": {"col": "temperature_2m_min", "method": "min", "desc": "Lowest temperature", "unit": "°C"},
    "max_temp": {"col": "temperature_2m_max", "method": "max", "desc": "Highest temperature", "unit": "°C"},
    "max_wind": {"col": "wind_speed_10m_max", "method": "max", "desc": "Strongest wind", "unit": "km/h"},
    "max_snow": {"col": "snowfall_sum", "method": "max", "desc": "Heaviest snowfall", "unit": "cm"},
    "max_rain": {"col": "rain_sum", "method": "max", "desc": "Heaviest rainfall", "unit": "mm"}
}

# --- LLM Prompts ---
INTENT_PARSER_SYSTEM_PROMPT = """You are a precise intent classification parser for a weather system.
Today is: {date_str}.

Your task is to extract parameters from the user's input and return a valid JSON object.

JSON FIELD SPECIFICATION:
1. 'is_weather_related': boolean.
   - Set to true if the query relates to weather, climate, atmospheric conditions, or specific weather events.
   - Set to false for unrelated topics.
2. 'city': string or null. The city name if specified.
3. 'date': string (YYYY-MM-DD) or null.
4. 'history_search': string or null. Use ONLY for past events.
   - Allowed values: 'rain', 'snow', 'wind', 'heat', 'frost', 'hail'.
5. 'record_search': string or null. Use ONLY for superlative record queries.
   - Allowed values: 'min_temp', 'max_temp', 'max_wind', 'max_snow', 'max_rain'.

Return ONLY the JSON object.
"""

RESPONSE_GENERATOR_SYSTEM_PROMPT = """You are a professional weather assistant.
Answer based EXCLUSIVELY on the provided 'Context' data. Do not hallucinate."""


# --- UI / Interface Configuration ---
UI_TITLE = "NeuroWeather GreyOps V3.0"
UI_HEADER = "// NEURO_WEATHER_CORE"

# Terminal-Style CSS
UI_CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Fira+Code:wght@400;700&display=swap');

:root {
    --terminal-orange: #ff6600;
    --terminal-bg: #1a1a1a;
    --terminal-panel: #262626;
    --terminal-glow: 0 0 8px rgba(255, 102, 0, 0.4);
}

body, .gradio-container {
    background-color: var(--terminal-bg) !important;
    color: var(--terminal-orange) !important;
    font-family: 'Fira Code', monospace !important;
}

.block, .panel, textarea, .output-markdown {
    background-color: var(--terminal-panel) !important;
    border: 1px solid #444 !important;
    color: var(--terminal-orange) !important;
}

#header-title {
    color: var(--terminal-orange);
    text-shadow: var(--terminal-glow);
    font-family: 'VT323', monospace;
    font-size: 3em;
    text-align: center;
    border-bottom: 2px solid var(--terminal-orange);
    padding-bottom: 10px;
    background-color: var(--terminal-panel);
}

button.primary-btn {
    background-color: var(--terminal-orange) !important;
    color: #1a1a1a !important;
    font-weight: bold;
    border: 1px solid var(--terminal-orange) !important;
}
footer { display: none !important; }
"""