from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from database import get_db
from utils.tmdb import populate_actors_for_movies, fetch_actors_by_names


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