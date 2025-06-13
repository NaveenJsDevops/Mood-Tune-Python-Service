from fastapi import FastAPI, HTTPException
from typing import Dict

from app.weather import fetch_current_weather_condition
from app.mood_matcher import is_mood_compatible_with_weather
from app.music import fetch_top_track_by_mood
from app.schemas import MoodRecommendationRequest, MoodRecommendationResponse
from app.utils import normalize_text

APP_TITLE = "Mood-Based Song Recommendation API"
APP_DESCRIPTION = (
    "Receives a user's mood and city, verifies compatibility with current weather, "
    "and recommends a song that suits the user's mood."
)
APP_VERSION = "1.0.0"

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)


@app.get("/ping", tags=["Health"])
def health_check() -> Dict[str, str]:
    """
    Simple health check endpoint to confirm API is operational.
    """
    return {"status": "ok"}


@app.post(
    "/recommendation",
    response_model=MoodRecommendationResponse,
    tags=["Recommendation"]
)
def generate_song_recommendation(request: MoodRecommendationRequest) -> MoodRecommendationResponse:
    """
    Processes mood and city input to determine weather-mood compatibility,
    then returns a song recommendation if the mood aligns with current weather.
    """
    if not request.mood.strip() or not request.city.strip():
        raise HTTPException(status_code=400, detail="Mood and city must be provided.")

    current_weather = fetch_current_weather_condition(request.city)
    if current_weather is None:
        raise HTTPException(status_code=404, detail="Could not fetch weather for the specified city.")

    normalized_mood = normalize_text(request.mood)
    is_mood_matched = is_mood_compatible_with_weather(normalized_mood, current_weather)
    song_recommendation = fetch_top_track_by_mood(normalized_mood) if is_mood_matched else None

    return MoodRecommendationResponse(
        city=request.city,
        weather=current_weather,
        mood=request.mood,
        mood_matches_weather=is_mood_matched,
        recommended_song=song_recommendation
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="192.168.180.251", port=8000, reload=True)
