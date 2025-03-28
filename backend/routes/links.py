from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Link
from schemas import LinkCreate, LinkResponse

router = APIRouter()

# 🔹 Ajouter un lien IMDb/TMDb
@router.post("/", response_model=LinkResponse)
def create_link(link: LinkCreate, db: Session = Depends(get_db)):
    new_link = Link(**link.model_dump())
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link

# 🔹 Récupérer un lien par movie_id
@router.get("/{movie_id}", response_model=LinkResponse)
def get_link(movie_id: int, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.movie_id == movie_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Lien non trouvé")
    return link