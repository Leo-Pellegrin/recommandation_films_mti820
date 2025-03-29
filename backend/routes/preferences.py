from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from models import Preference, UserMoviePreference
from schemas import GenreList, ActorList, MovieIDList, MovieResponse

router = APIRouter(prefix="", tags=["Preferences"])

# --- ALL --- 
@router.get("/{user_id}")
def get_all_preferences(user_id: int, db: Session = Depends(get_db)):
    pref = db.query(Preference).filter_by(user_id=user_id).first()
    if not pref:
        raise HTTPException(status_code=404, detail="Preferences not found")

    favorites = (
        db.query(UserMoviePreference)
        .options(joinedload(UserMoviePreference.movie))
        .filter(UserMoviePreference.user_id == user_id)
        .all()
    )

    favorite_movies = [
        {
            "movie_id": fav.movie.movie_id,
            "title": fav.movie.title,
            "poster_path": fav.movie.poster_path or "/images/placeholder_movie.jpeg",
            "year": fav.movie.year,
            "genres": fav.movie.genres or []
        }
        for fav in favorites
    ]

    return {
        "genres": pref.preferred_genres or [],
        "actors": pref.preferred_actors or [],
        "favorite_movies": favorite_movies
    }

# --- GENRES ---

@router.get("/{user_id}/genres")
def get_user_genres(user_id: int, db: Session = Depends(get_db)):
    pref = db.query(Preference).filter_by(user_id=user_id).first()
    if not pref:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return {"preferred_genres": pref.preferred_genres}

@router.post("/{user_id}/genres")
def set_user_genres(user_id: int, data: GenreList, db: Session = Depends(get_db)):
    pref = db.query(Preference).filter_by(user_id=user_id).first()
    if not pref:
        pref = Preference(user_id=user_id, preferred_genres=data.genres)
        db.add(pref)
    else:
        pref.preferred_genres = data.genres
    db.commit()
    return {"message": "Preferred genres updated"}

@router.delete("/{user_id}/genres/{genre}")
def delete_user_genre(user_id: int, genre: str, db: Session = Depends(get_db)):
    pref = db.query(Preference).filter_by(user_id=user_id).first()
    if not pref:
        raise HTTPException(status_code=404, detail="Preferences not found")

    # Normalisation pour comparaison insensible à la casse
    normalized_genre = genre.strip().lower()
    updated_genres = [g for g in pref.preferred_genres if g.strip().lower() != normalized_genre]

    if len(updated_genres) == len(pref.preferred_genres):
        raise HTTPException(status_code=404, detail="Genre not found in preferences")

    pref.preferred_genres = updated_genres
    db.commit()
    return {"message": f"Genre '{genre}' removed from preferences"}

# --- ACTORS ---

@router.get("/{user_id}/actors")
def get_user_actors(user_id: int, db: Session = Depends(get_db)):
    pref = db.query(Preference).filter_by(user_id=user_id).first()
    if not pref:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return {"preferred_actors": pref.preferred_actors}

@router.post("/{user_id}/actors")
def set_user_actors(user_id: int, data: ActorList, db: Session = Depends(get_db)):
    pref = db.query(Preference).filter_by(user_id=user_id).first()
    if not pref:
        pref = Preference(user_id=user_id, preferred_actors=data.actors)
        db.add(pref)
    else:
        pref.preferred_actors = data.actors
    db.commit()
    return {"message": "Preferred actors updated"}

@router.delete("/{user_id}/actors/{actor}")
def delete_user_actor(user_id: int, actor: str, db: Session = Depends(get_db)):
    pref = db.query(Preference).filter_by(user_id=user_id).first()
    if not pref:
        raise HTTPException(status_code=404, detail="Preferences not found")

    normalized_actor = actor.strip().lower()
    updated_actors = [a for a in pref.preferred_actors if a.strip().lower() != normalized_actor]

    if len(updated_actors) == len(pref.preferred_actors):
        raise HTTPException(status_code=404, detail="Actor not found in preferences")

    pref.preferred_actors = updated_actors
    db.commit()
    return {"message": f"Actor '{actor}' removed from preferences"}
# --- AJOUT MULTIPLE DE FILMS FAVORIS ---

@router.get("/{user_id}/favorites/movies", response_model=List[MovieResponse])
def get_favorite_movies(user_id: int, db: Session = Depends(get_db)):
    favorites = (
        db.query(UserMoviePreference)
        .options(joinedload(UserMoviePreference.movie))  # charge les infos du film
        .filter(UserMoviePreference.user_id == user_id)
        .all()
    )

    if not favorites:
        raise HTTPException(status_code=404, detail="No favorite movies found")

    return [
        {
            "movie_id": fav.movie.movie_id,
            "title": fav.movie.title,
            "poster_path": fav.movie.poster_path or "/images/placeholder_movie.jpeg",
            "year": fav.movie.year,
            "genres": fav.movie.genres or []
        }
        for fav in favorites
    ]

@router.post("/{user_id}/favorites/movies/batch")
def add_multiple_favorite_movies(user_id: int, data: MovieIDList, db: Session = Depends(get_db)):
    for movie_id in data.movie_ids:
        exists = db.query(UserMoviePreference).filter_by(user_id=user_id, movie_id=movie_id).first()
        if not exists:
            db.add(UserMoviePreference(user_id=user_id, movie_id=movie_id))
    db.commit()
    return {"message": f"{len(data.movie_ids)} movies added to favorites"}

@router.delete("/{user_id}/favorites/movies/{movie_id}")
def remove_favorite_movie(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    rel = db.query(UserMoviePreference).filter_by(user_id=user_id, movie_id=movie_id).first()
    if not rel:
        raise HTTPException(status_code=404, detail="Movie not found in favorites")
    db.delete(rel)
    db.commit()
    return {"message": "Movie removed from favorites"}

@router.delete("/{user_id}/favorites/movies/batch")
def remove_multiple_favorite_movies(user_id: int, data: MovieIDList, db: Session = Depends(get_db)):
    deleted = 0
    for movie_id in data.movie_ids:
        rel = db.query(UserMoviePreference).filter_by(user_id=user_id, movie_id=movie_id).first()
        if rel:
            db.delete(rel)
            deleted += 1
    db.commit()
    return {"message": f"{deleted} movies removed from favorites"}