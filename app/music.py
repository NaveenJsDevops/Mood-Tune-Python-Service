import os
import requests
from typing import Optional, Dict

# Load environment variables from .env only in local dev
if os.getenv("RENDER") != "true":
    from dotenv import load_dotenv
    load_dotenv()

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def fetch_top_track_by_mood(mood_tag: str) -> Optional[Dict[str, str]]:
    """
    Fetch the top track for a given mood tag from the Last.fm API.

    Args:
        mood_tag (str): The mood to search songs for (used as a tag).

    Returns:
        Optional[Dict[str, str]]: A dictionary with 'title' and 'artist' or None.
    """
    params = {
        "method": "tag.gettoptracks",
        "tag": mood_tag.lower(),
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": 1
    }

    try:
        response = requests.get(LASTFM_BASE_URL, params=params)
        response.raise_for_status()
        tracks = response.json().get("tracks", {}).get("track", [])
        if not tracks:
            return None

        top_track = tracks[0]
        return {
            "title": top_track["name"],
            "artist": top_track["artist"]["name"]
        }

    except (requests.RequestException, KeyError, IndexError):
        return None
