from pydantic import BaseModel, Field
from typing import Union, Dict

class MoodRecommendationRequest(BaseModel):
    mood: str = Field(..., description="User's current mood, e.g., happy, sad")
    city: str = Field(..., description="City name for weather lookup")

class MoodRecommendationResponse(BaseModel):
    city: str
    weather: str
    mood: str
    mood_matches_weather: bool
    recommended_song: Union[Dict[str, str], None]
