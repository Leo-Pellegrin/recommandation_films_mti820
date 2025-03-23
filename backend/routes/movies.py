from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Movie
from schemas import MovieCreate, MovieResponse, GenresResponse
from typing import List

router = APIRouter()


@router.get("/genres", response_model=List[str])
def get_genres(db: Session = Depends(get_db)):
    genres = db.query(Movie.genres).distinct().all()

    unique_genres = set()  # Utiliser un `set` pour éviter les doublons

    for genre_list in genres:
        if genre_list[0]:  
            genre_items = eval(genre_list[0]) if isinstance(genre_list[0], str) else genre_list[0]
            unique_genres.update(genre_items)  # Ajoute chaque genre unique

    return sorted(unique_genres)  # Retourne une liste triée pour plus de lisibilité


# 🔹 Ajouter un film
@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    new_movie = Movie(**movie.model_dump())  # ✅ Correction ici
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

# 🔹 Récupérer tous les films
@router.get("/", response_model=List[MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

# 🔹 Récupérer un film par ID
@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return movie

@router.get("/{movie_id}/recommendations", response_model=List[MovieResponse])
def get_recommendations(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    recommendations = db.query(Movie).filter(Movie.movie_id != movie_id).all()
    return recommendations

@router.get("/search/{title}", response_model=List[MovieResponse])
def search_movies(title: str, db: Session = Depends(get_db)):
    movies = db.query(Movie).filter(Movie.title.ilike(f"%{title}%")).all()
    return movies

@router.get("{movie_id}/links", response_model=List[MovieResponse])
def get_links(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    links = db.query(Movie).filter(Movie.movie_id != movie_id).all()
    return links
