import logging
from datetime import date
from typing import Optional, List

logger = logging.getLogger("NeuroWeather")


class ConversationState:
    """Maintains the context of the user session (location and time)."""

    def __init__(self) -> None:
        self.last_city_name: Optional[str] = None
        self.last_coords: Optional[List[float]] = None
        self.last_date: Optional[date] = None

    def update(self, city: Optional[str], coords: Optional[List[float]], query_date: Optional[date]) -> None:
        """Updates the state with new information if provided."""
        if city and coords:
            self.last_city_name = city
            self.last_coords = coords
        if query_date:
            self.last_date = query_date

        logger.debug(f"State Updated: City={self.last_city_name}, Date={self.last_date}")