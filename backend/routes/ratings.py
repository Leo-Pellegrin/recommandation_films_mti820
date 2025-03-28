from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Rating
from schemas import RatingCreate, RatingResponse
from typing import List
from sqlalchemy.sql import func

router = APIRouter()

# 🔹 Ajouter une notation
@router.post("/", response_model=RatingResponse)
def add_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    new_rating = Rating(**rating.model_dump())
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return {"id": new_rating.rating_id, "user_id": new_rating.user_id, "movie_id": new_rating.movie_id, "rating": new_rating.rating} 

# 🔹 Récupérer les notations d'un utilisateur
@router.get("/user/{user_id}", response_model=List[RatingResponse])
def get_user_ratings(user_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    return [{"id": r.rating_id, "user_id": r.user_id, "movie_id": r.movie_id, "rating": r.rating} for r in ratings] 

@router.post("/user/{user_id}")
def add_user_rating(user_id: int, ratings: List[RatingCreate], db: Session = Depends(get_db)):
    for rating in ratings:
        new_rating = Rating(**rating.model_dump())
        new_rating.user_id = user_id
        db.add(new_rating)
    db.commit()
    return {"message": "Notations ajoutées avec succès"}

# 🔹 Récupérer la moyenne d’un film
@router.get("/movie/{movie_id}/average")
def get_average_rating(movie_id: int, db: Session = Depends(get_db)):
    avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.movie_id == movie_id).scalar()
    return {"movie_id": movie_id, "average_rating": avg_rating}