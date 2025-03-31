from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from database import get_db
from utils.tmdb import populate_actors_for_movies, fetch_actors_by_names
from models import Movie, Link
from utils.tmdb import fetch_tmdb_details


router = APIRouter(prefix="", tags=["Tools"])

@router.post("/populate-actors")
def populate_actors(db: Session = Depends(get_db)):
    populate_actors_for_movies(db)
    return {"message": "Actors updated for all movies"}

@router.post("/actors/by-names")
def get_actors_by_names(payload: dict = Body(...)):
    names = payload.get("names", [])
    actors = fetch_actors_by_names(names)
    return {"actors": actors}

@router.post("/movies/poster")
def get_posters_for_movies(db: Session = Depends(get_db)):
    # Récupère les films sans poster avec leur lien TMDB
    movies = (
        db.query(Movie)
        .join(Link, Movie.movie_id == Link.movie_id)
        .filter(Movie.poster_path == None)
        .all()
    )

    updated = 0

    for movie in movies:
        tmdb_id = db.query(Link).filter(Link.movie_id == movie.movie_id).first().tmdb_id
        if not tmdb_id:
            continue

        try:
            details = fetch_tmdb_details(tmdb_id)
            if details.get("poster_path"):
                movie.poster_path = details["poster_path"]
                updated += 1
        except Exception as e:
            print(f"❌ Erreur pour le film ID {movie.movie_id} / TMDB {tmdb_id} : {e}")

    db.commit()
    return {"message": f"{updated} poster(s) mis à jour avec succès."}