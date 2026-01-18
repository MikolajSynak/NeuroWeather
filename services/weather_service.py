import pandas as pd
from datetime import date, timedelta
from typing import List
from data.data_getter import get_hourly_forecast, get_historical_weather_data
from settings import config


class WeatherService:
    """Domain service for interpreting weather data and generating context strings."""

    @staticmethod
    def _get_wmo_description(code: int) -> str:
        """Translates WMO integer code to string description."""
        return config.WMO_CODES.get(int(code), "Unknown")

    @classmethod
    def find_historical_event(cls, city_coords: List[float], event_type: str) -> str:
        """Searches for the last occurrence of a specific weather event.

        Args:
            city_coords: [lat, lon]
            event_type: Key from config.SEARCH_CONFIG (e.g., 'snow', 'rain').

        Returns:
            str: Human-readable context string regarding the event.
        """
        search_cfg = config.SEARCH_CONFIG.get(event_type)
        if not search_cfg:
            return f"Event type '{event_type}' is not configured."

        today = date.today()
        # Search window: 2 years (730 days)
        df = get_historical_weather_data(str(today - timedelta(days=730)), str(today), city_coords)

        if isinstance(df, dict) or df.empty:
            return "Error retrieving historical data."

        col = search_cfg["col"]
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Apply filtering logic based on operator
        operator = search_cfg["op"]
        threshold = search_cfg["val"]

        if operator == ">":
            matches = df[df[col] > threshold]
        elif operator == "<":
            matches = df[df[col] < threshold]
        elif operator == "in":
            matches = df[df[col].isin(threshold)]
        else:
            return "Invalid configuration operator."

        if matches.empty:
            return f"No occurrence of {search_cfg['desc']} found in the last 2 years."

        last_event = matches.sort_values(by='date', ascending=False).iloc[0]
        val_display = last_event[col]

        if col == "weather_code":
            val_display = cls._get_wmo_description(val_display)

        return (
            f"HISTORICAL ANALYSIS ({search_cfg['desc']}):\n"
            f"Last occurrence date: {last_event['date'].date()}\n"
            f"Measured value: {val_display} {search_cfg.get('unit', '')}"
        )

    @classmethod
    def find_all_time_record(cls, city_coords: List[float], record_type: str) -> str:
        """Searches for weather records since 1960.

        Args:
            city_coords: [lat, lon]
            record_type: Key from config.RECORD_CONFIG.

        Returns:
            str: Human-readable context string.
        """
        record_cfg = config.RECORD_CONFIG.get(record_type)
        if not record_cfg:
            return f"Record type '{record_type}' is not configured."

        today = date.today()
        start_date = "1960-01-01"

        df = get_historical_weather_data(start_date, str(today), city_coords)

        if isinstance(df, dict) or df.empty:
            return "Error retrieving historical archive."

        col = record_cfg["col"]
        df[col] = pd.to_numeric(df[col], errors='coerce')

        if record_cfg["method"] == "max":
            idx = df[col].idxmax()
        else:
            idx = df[col].idxmin()

        if pd.isna(idx):
            return "No valid data found for this record type."

        record_row = df.loc[idx]
        val = round(float(record_row[col]), 1)

        return (
            f"HISTORICAL RECORD (Since 1960 - {record_cfg['desc']}):\n"
            f"Date: {record_row['date'].date()}\n"
            f"Value: {val} {record_cfg['unit']}"
        )

    @classmethod
    def get_weather_context(cls, city_coords: List[float], query_date: date) -> str:
        """Retrieves standard forecast or historical report for a specific date.

        Args:
            city_coords: [lat, lon]
            query_date: The date object to query.

        Returns:
            str: Context string for the LLM.
        """
        today = date.today()

        try:
            if query_date < today:
                # Historical Query
                df = get_historical_weather_data(str(query_date), str(query_date), city_coords)
                if isinstance(df, dict) or df.empty:
                    return "No data available for this date."

                row = df.iloc[0]
                condition = cls._get_wmo_description(row.get('weather_code', 0))

                return (
                    f"Historical Report ({query_date}):\n"
                    f"Condition: {condition}\n"
                    f"Temp Range: {row.get('temperature_2m_min', '?')}°C to {row.get('temperature_2m_max', '?')}°C\n"
                    f"Precipitation: {row.get('rain_sum', 0)} mm\n"
                    f"Max Wind: {row.get('wind_speed_10m_max', 0)} km/h"
                )
            else:
                # Forecast Query
                df = get_hourly_forecast(city_coords, forecast_days=16)
                if df.empty:
                    return "Forecast API error."

                df['date'] = pd.to_datetime(df['date']).dt.date
                day_data = df[df['date'] == query_date]

                if day_data.empty:
                    return f"Date {query_date} is out of forecast range (max 16 days)."

                return (
                    f"Forecast ({query_date}):\n"
                    f"Temp Range: {day_data['temperature_2m'].min():.1f}°C to {day_data['temperature_2m'].max():.1f}°C\n"
                    f"Precipitation Probability: {day_data['precipitation_probability'].max()}%\n"
                    f"Max Wind: {day_data['wind_speed_10m'].max():.1f} km/h"
                )

        except Exception as e:
            return f"Data processing error: {str(e)}"