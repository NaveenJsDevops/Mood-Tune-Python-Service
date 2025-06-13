import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)


@pytest.fixture
def mock_dependencies():
    with patch("app.weather.fetch_current_weather_condition") as mock_weather, \
            patch("app.music.fetch_top_track_by_mood") as mock_music, \
            patch("app.utils.normalize_text") as mock_normalize, \
            patch("app.mood_matcher.is_mood_compatible_with_weather") as mock_matcher:

        mock_weather.return_value = "Clear"
        mock_music.return_value = {"title": "Happy Song", "artist": "Good Vibes"}
        mock_normalize.side_effect = lambda x: x.strip().lower()
        mock_matcher.return_value = True

        yield


def test_health_check():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("main.fetch_current_weather_condition", return_value="Clear")
@patch("main.fetch_top_track_by_mood", return_value={"title": "Happy Song", "artist": "Good Vibes"})
@patch("main.normalize_text", side_effect=lambda x: x.strip().lower())
@patch("main.is_mood_compatible_with_weather", return_value=True)
def test_generate_song_recommendation_success(mock_matcher, mock_normalize, mock_music, mock_weather):
    request_payload = {
        "mood": "Happy",
        "city": "London"
    }
    response = client.post("/recommendation", json=request_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "London"
    assert data["mood"] == "Happy"
    assert data["weather"] == "Clear"
    assert data["mood_matches_weather"] is True
    assert data["recommended_song"] == {"title": "Happy Song", "artist": "Good Vibes"}


def test_generate_song_recommendation_invalid_input():
    response = client.post("/recommendation", json={"mood": "", "city": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Mood and city must be provided."
