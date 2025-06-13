import os
import requests
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_current_weather_condition(city_name: str) -> Optional[str]:
    """
    Retrieves the main weather condition for the specified city using OpenWeatherMap.

    Args:
        city_name (str): City for which to fetch the weather.

    Returns:
        Optional[str]: Weather condition (e.g., 'Clear', 'Rain'), or None if failed.
    """
    params = {
        "q": city_name,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(OPENWEATHER_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()["weather"][0]["main"]
    except (requests.RequestException, KeyError, IndexError):
        return None
