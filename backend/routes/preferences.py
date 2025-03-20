# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import get_db
# from models import UserPreferences
# from schemas import UserPreferencesCreate, UserPreferencesResponse

# router = APIRouter()

# # 🔹 Ajouter ou mettre à jour les préférences d'un utilisateur
# @router.post("/", response_model=UserPreferencesResponse)
# def update_preferences(preferences: UserPreferencesCreate, db: Session = Depends(get_db)):
#     existing = db.query(UserPreferences).filter(UserPreferences.user_id == preferences.user_id).first()
#     if existing:
#         existing.favorite_genres = preferences.favorite_genres
#     else:
#         existing = UserPreferences(**preferences.model_dump())
#         db.add(existing)
#     db.commit()
#     db.refresh(existing)
#     return existing

# # 🔹 Récupérer les préférences d’un utilisateur
# @router.get("/{user_id}", response_model=UserPreferencesResponse)
# def get_preferences(user_id: int, db: Session = Depends(get_db)):
#     preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
#     if not preferences:
#         raise HTTPException(status_code=404, detail="Préférences non trouvées")
#     return preferences