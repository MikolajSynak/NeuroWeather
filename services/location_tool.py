from typing import Tuple, Optional, List
from thefuzz import process, fuzz
from settings.cities import CITY_COORDINATES
from settings import config


class LocationFinder:
    """Service for resolving fuzzy city names to geo-coordinates."""

    def __init__(self) -> None:
        self.city_names: List[str] = list(CITY_COORDINATES.keys())

    def find_coordinates(self, city_query: str) -> Tuple[Optional[str], Optional[List[float]]]:
        """Matches a user provided city string to the database.

        Args:
            city_query: The city name extracted from user input.

        Returns:
            Tuple[Optional[str], Optional[List[float]]]:
                (City Name, [lat, lon]) if found, otherwise (None, None).
        """
        if not city_query:
            return None, None

        best_match = process.extractOne(
            city_query,
            self.city_names,
            scorer=fuzz.ratio
        )

        if best_match and best_match[1] >= config.FUZZY_MATCH_THRESHOLD:
            city_name = best_match[0]
            coordinates = CITY_COORDINATES[city_name]
            return city_name, coordinates

        return None, None