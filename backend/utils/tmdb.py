import requests
import os
from models import Movie, Link
from sqlalchemy.orm import Session

TMDB_API_KEY = "166e544a3195c0c362b7c9294e90775d"
TMDB_API_BASE = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w185"
TMDB_FULL_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w780"

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
    
def fetch_tmdb_full_details(tmdb_id: int):
    try:
        response = requests.get(
            f"{TMDB_API_BASE}/movie/{tmdb_id}",
            params={
                "api_key": TMDB_API_KEY,
                "language": "en-US",
                "append_to_response": "credits,similar"
            }
        )
        data = response.json()

        return {
            "backdrop_path": f"{TMDB_FULL_IMAGE_BASE_URL}{data['backdrop_path']}" if data.get("backdrop_path") else None,
            "summary": data.get("overview"),
            "runtime": data.get("runtime"),
            "cast": [actor["name"] for actor in data.get("credits", {}).get("cast", [])[:3]],
            "similar": [
                {
                    "id": movie["id"],
                    "title": movie["title"],
                    "backdrop_path": f"{TMDB_FULL_IMAGE_BASE_URL}{movie['backdrop_path']}"
                    if movie.get("backdrop_path") else None
                }
                for movie in data.get("similar", {}).get("results", [])[:10]
            ]
        }

    except Exception as e:
        print(f"[TMDB] Erreur fetch full details for {tmdb_id}:", e)
        return {}
    
def fetch_poster_from_tmdb(tmdb_id: int):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{tmdb_id}",
            params={"api_key": TMDB_API_KEY, "language": "en-US"}
        )
        data = response.json()
        return f"{TMDB_IMAGE_BASE_URL}{data['poster_path']}" if data.get("poster_path") else None
    except Exception as e:
        print(f"❌ TMDB error for ID {tmdb_id}: {e}")
        return None
    
def populate_actors_for_movies(db: Session):
    movies = db.query(Movie).all()

    for movie in movies:
        link = db.query(Link).filter(Link.movie_id == movie.movie_id).first()
        if not link or not link.tmdb_id:
            continue
        
        try:
            response = requests.get(
                f"https://api.themoviedb.org/3/movie/{link.tmdb_id}",
                params={"api_key": TMDB_API_KEY, "language": "en-US", "append_to_response": "credits"}
            )
            data = response.json()
            cast = [actor["name"] for actor in data.get("credits", {}).get("cast", [])[:3]]
            movie.actors = cast
            print(f"✅ {movie.title} : {cast}")
        except Exception as e:
            print(f"❌ Erreur pour le film ID {movie.movie_id} : {e}")

    db.commit()
    
def fetch_actors_by_names(names: list[str]) -> list[dict]:
    results = []

    for name in names:
        try:
            response = requests.get(
                "https://api.themoviedb.org/3/search/person",
                params={
                    "api_key": TMDB_API_KEY,
                    "query": name,
                    "language": "en-US",
                    "page": 1
                }
            )
            data = response.json()
            person = data.get("results", [])[0] if data.get("results") else None

            if person:
                results.append({
                    "id": person["id"],
                    "name": person["name"],
                    "profile_path": f"{TMDB_IMAGE_BASE_URL}{person['profile_path']}" if person.get("profile_path") else None
                })

        except Exception as e:
            print(f"Erreur TMDB lors de la recherche de '{name}': {e}")

    return results