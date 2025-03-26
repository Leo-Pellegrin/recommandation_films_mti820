from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Movie
from schemas import MovieResponse
from typing import List

from services.recommandations import get_collaborative_recommendations, get_content_based_recommendations, get_hybrid_recommendations

router = APIRouter()

@router.get("/collaborative/{user_id}", response_model=List[MovieResponse])
def recommend_collaborative(user_id: int, db: Session = Depends(get_db)):
    movies = get_collaborative_recommendations(user_id, db)
    if not movies:
        raise HTTPException(status_code=404, detail="Aucune recommandation collaborative trouvée.")
    return movies

@router.get("/content/{user_id}", response_model=List[MovieResponse])
def recommend_content_based(user_id: int, db: Session = Depends(get_db)):
    movies = get_content_based_recommendations(user_id, db)
    if not movies:
        raise HTTPException(status_code=404, detail="Aucune recommandation basée sur le contenu trouvée.")
    return movies

@router.get("/hybrid/{user_id}", response_model=List[MovieResponse])
def recommend_hybrid(user_id: int, db: Session = Depends(get_db)):
    movies = get_hybrid_recommendations(user_id, db)
    if not movies:
        raise HTTPException(status_code=404, detail="Aucune recommandation hybride trouvée.")
    return movies
