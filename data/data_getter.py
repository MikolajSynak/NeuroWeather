import pandas as pd
import requests_cache
import openmeteo_requests
from retry_requests import retry
from typing import List, Union, Dict, Any
from settings import config

# Initialize API Client
cache_session = requests_cache.CachedSession(config.CACHE_NAME, expire_after=config.CACHE_EXPIRE_AFTER)
retry_session = retry(cache_session, retries=config.RETRY_COUNT, backoff_factor=config.RETRY_BACKOFF)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_hourly_forecast(city_coords: List[float], forecast_days: int = 3) -> pd.DataFrame:
    """Fetches hourly forecast data from Open-Meteo API.

    Args:
        city_coords: A list containing [latitude, longitude].
        forecast_days: Number of days to forecast (1-16).

    Returns:
        pd.DataFrame: DataFrame containing hourly weather variables.
                      Returns empty DataFrame on API failure.

    Raises:
        ValueError: If city_coords is invalid.
    """
    if not city_coords or len(city_coords) < 2:
        raise ValueError("Invalid coordinates provided.")

    params = {
        "latitude": city_coords[0],
        "longitude": city_coords[1],
        "hourly": config.HOURLY_VARIABLES,
        "timezone": "auto",
        "forecast_days": forecast_days
    }

    try:
        responses = openmeteo.weather_api(config.OPEN_METEO_FORECAST_URL, params=params)
        response = responses[0]

        hourly = response.Hourly()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            )
        }

        for i, var_name in enumerate(config.HOURLY_VARIABLES):
            hourly_data[var_name] = hourly.Variables(i).ValuesAsNumpy()

        return pd.DataFrame(data=hourly_data)

    except Exception:
        return pd.DataFrame()


def get_historical_weather_data(
        start_date: str,
        end_date: str,
        city_coords: List[float]
) -> Union[pd.DataFrame, Dict[str, Any]]:
    """Fetches historical daily weather data.

    Args:
        start_date: String YYYY-MM-DD.
        end_date: String YYYY-MM-DD.
        city_coords: [latitude, longitude].

    Returns:
        Union[pd.DataFrame, Dict[str, Any]]: DataFrame with weather data or Dict with error info.
    """
    params = {
        "latitude": city_coords[0],
        "longitude": city_coords[1],
        "start_date": start_date,
        "end_date": end_date,
        "daily": config.DAILY_VARIABLES
    }

    try:
        responses = openmeteo.weather_api(config.OPEN_METEO_ARCHIVE_URL, params=params)
        response = responses[0]

        daily = response.Daily()
        daily_data = {}

        for i, var_name in enumerate(config.DAILY_VARIABLES):
            daily_data[var_name] = daily.Variables(i).ValuesAsNumpy()

        daily_data["date"] = pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )

        return pd.DataFrame(data=daily_data)

    except Exception as e:
        return {"error": True, "reason": str(e)}
