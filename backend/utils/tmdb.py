import requests
import os

TMDB_API_KEY = "166e544a3195c0c362b7c9294e90775d"
TMDB_API_BASE = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w185"

def fetch_tmdb_details(tmdb_id: int):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{tmdb_id}",
            params={"api_key": TMDB_API_KEY, "language": "en-US"}
        )        
        data = response.json()
        return {
            "poster_path": f"{TMDB_IMAGE_BASE_URL}{data['poster_path']}" if data.get("poster_path") else None,
            "year": int(data["release_date"][:4]) if data.get("release_date") else None,
            "genres": [g["name"] for g in data.get("genres", [])]
        }
    except Exception as e:
        print(f"[TMDB] Erreur fetch details for {tmdb_id} :", e)
        return {}