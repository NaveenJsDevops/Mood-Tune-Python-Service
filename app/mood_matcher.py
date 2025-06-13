from typing import Dict, List

MOOD_TO_WEATHER_MAP: Dict[str, List[str]] = {
    "happy": ["Clear", "Sunny"],
    "sad": ["Rain", "Drizzle", "Clouds"],
    "angry": ["Thunderstorm", "Wind"],
    "calm": ["Clear", "Clouds"],
    "anxious": ["Fog", "Mist"],
    "romantic": ["Clear", "Rain", "Clouds"]
}

def is_mood_compatible_with_weather(mood: str, weather_condition: str) -> bool:
    """
    Determines if the user's mood is typically associated with the given weather.

    Args:
        mood (str): The user's mood.
        weather_condition (str): The current weather condition.

    Returns:
        bool: True if the mood is compatible with the weather.
    """
    mood = mood.lower()
    weather_condition = weather_condition.capitalize()
    return weather_condition in MOOD_TO_WEATHER_MAP.get(mood, [])
