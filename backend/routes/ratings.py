from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Rating
from schemas import RatingCreate, RatingResponse
from typing import List
from sqlalchemy.sql import func
from datetime import datetime
from models import Rating, Movie, Link
from utils.tmdb import fetch_poster_from_tmdb


router = APIRouter()

# 🔹 Ajouter une notation
@router.post("/", response_model=RatingResponse)
def add_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    new_rating = Rating(**rating.model_dump())
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return {"id": new_rating.rating_id, "user_id": new_rating.user_id, "movie_id": new_rating.movie_id, "rating": new_rating.rating} 

# Récupérer tout les ratings de l'utilisateur
@router.get("/user/{user_id}")
def get_user_ratings(user_id: int, db: Session = Depends(get_db)):
    ratings = (
        db.query(Rating)
        .join(Movie)
        .outerjoin(Link, Movie.movie_id == Link.movie_id)
        .options(joinedload(Rating.movie))
        .filter(Rating.user_id == user_id)
        .all()
    )

    result = []
    for r in ratings:
        poster_path = r.movie.poster_path
        if not poster_path and r.movie.link:
            poster_path = fetch_poster_from_tmdb(r.movie.link.tmdb_id)

        result.append({
            "movie_id": r.movie.movie_id,
            "title": r.movie.title,
            "rating": r.rating,
            "poster_path": poster_path or "/images/placeholder_movie.jpeg"
        })

    return result

# Ajouter plusieurs ratings
@router.post("/user/{user_id}/ratings")
def add_user_ratings(user_id: int, ratings: List[RatingCreate], db: Session = Depends(get_db)):
    for rating in ratings:
        new_rating = Rating(
            user_id=user_id,
            movie_id=rating.movie_id,
            rating=rating.rating,
            timestamp=rating.timestamp or datetime.now
        )
        db.add(new_rating)
    db.commit()
    return {"message": f"{len(ratings)} notations ajoutées avec succès"}

# Ajouter un rating
@router.post("/user/{user_id}/rating")
def add_single_user_rating(user_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    new_rating = Rating(
        user_id=user_id,
        movie_id=rating.movie_id,
        rating=rating.rating,
        timestamp=rating.timestamp or datetime.utcnow()  # fallback si non fourni
    )
    db.add(new_rating)
    db.commit()
    return {"message": "Notation ajoutée avec succès"}

# 🔹 Récupérer la moyenne d’un film
@router.get("/movie/{movie_id}/average")
def get_average_rating(movie_id: int, db: Session = Depends(get_db)):
    avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.movie_id == movie_id).scalar()
    return {"movie_id": movie_id, "average_rating": avg_rating}