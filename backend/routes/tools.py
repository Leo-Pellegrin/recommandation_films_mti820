from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from utils.tmdb import populate_actors_for_movies

router = APIRouter(prefix="", tags=["Tools"])

@router.post("/populate-actors")
def populate_actors(db: Session = Depends(get_db)):
    populate_actors_for_movies(db)
    return {"message": "Actors updated for all movies"}