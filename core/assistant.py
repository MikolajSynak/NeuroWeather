import json
import logging
from datetime import date, datetime
from typing import Optional, Dict, Tuple, Any, List

from groq import Groq
from settings import config
from services.location_tool import LocationFinder
from services.weather_service import WeatherService
from core.state import ConversationState

logger = logging.getLogger("NeuroWeather")


class WeatherAssistant:
    """Controller class for the NeuroWeather Agent."""

    def __init__(self) -> None:
        self._validate_env()
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.finder = LocationFinder()
        self.state = ConversationState()

    def _validate_env(self) -> None:
        """Checks for required environment variables."""
        if not config.GROQ_API_KEY:
            logger.critical("GROQ_API_KEY is missing in environment variables.")
            exit(1)

    def _get_intent(self, user_prompt: str) -> Dict[str, Any]:
        """Invokes LLM to parse user intent into structured JSON.

        Args:
            user_prompt: Raw input from user.

        Returns:
            Dict: Parsed JSON intent.
        """
        today_str = str(date.today())
        system_prompt = config.INTENT_PARSER_SYSTEM_PROMPT.format(date_str=today_str)

        try:
            completion = self.client.chat.completions.create(
                model=config.LLM_MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            content = completion.choices[0].message.content
            return json.loads(content) if content else {}
        except Exception as e:
            logger.error(f"Intent parsing failed: {e}")
            return {"is_weather_related": False}

    def _resolve_context(self, intent: Dict[str, Any]) -> Tuple[Optional[str], Optional[List[float]], Optional[date]]:
        """Resolves City and Date context using State Fallback."""
        extracted_city = intent.get("city")
        extracted_date = intent.get("date")

        final_city, final_coords, final_date = None, None, None

        # Resolve City
        if extracted_city:
            final_city, final_coords = self.finder.find_coordinates(extracted_city)
            if not final_city:
                logger.warning(f"City '{extracted_city}' not found in database.")

        # Fallback
        if not final_city:
            final_city = self.state.last_city_name
            final_coords = self.state.last_coords

        # Resolve Date
        if extracted_date:
            try:
                final_date = datetime.strptime(extracted_date, "%Y-%m-%d").date()
            except ValueError:
                logger.error(f"Invalid date format from LLM: {extracted_date}")

        # Fallback
        if not final_date:
            final_date = self.state.last_date if self.state.last_date else date.today()

        return final_city, final_coords, final_date

    def _fetch_weather_data(self, intent: Dict[str, Any], coords: List[float], query_date: date) -> str:
        """Routes the query to the correct service method based on intent."""
        record_type = intent.get("record_search")
        hist_type = intent.get("history_search")

        if record_type:
            logger.info(f"Executing Record Search: {record_type}")
            return WeatherService.find_all_time_record(coords, record_type)

        if hist_type:
            logger.info(f"Executing Historical Event Search: {hist_type}")
            return WeatherService.find_historical_event(coords, hist_type)

        logger.info(f"Executing Standard Report: {query_date}")
        return WeatherService.get_weather_context(coords, query_date)

    def process_query(self, user_prompt: str) -> str:
        """Main processing pipeline."""
        # 1. Intent Analysis
        intent = self._get_intent(user_prompt)
        logger.debug(f"Intent JSON: {intent}")

        if not intent.get("is_weather_related", False):
            return "This query does not appear to be weather-related."

        # 2. Context Resolution
        city_name, coords, query_date = self._resolve_context(intent)

        if not city_name or not coords:
            return "I could not identify the city. Please specify the location."

        self.state.update(city_name, coords, query_date)

        # 3. Data Retrieval
        context_data = self._fetch_weather_data(intent, coords, query_date)

        # 4. Response Generation
        user_message = f"Context (City: {city_name}): {context_data}\n\nUser Question: {user_prompt}"

        completion = self.client.chat.completions.create(
            model=config.LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": config.RESPONSE_GENERATOR_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=300
        )

        content = completion.choices[0].message.content
        return content if content else "Error generating response."