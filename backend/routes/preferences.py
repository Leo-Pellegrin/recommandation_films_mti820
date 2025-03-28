# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import get_db
# from models import UserPreferences
# from schemas import UserPreferencesCreate, UserPreferencesResponse

# router = APIRouter()

# # 🔹 Ajouter ou mettre à jour les préférences d'un utilisateur
# @router.post("/movies/{user_id}", response_model=UserPreferencesResponse)
# def add_movies_preferences(movie_prefenrences: UserPreferencesCreate, user_id: int, db: Session = Depends(get_db)):
#     preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
#     if not preferences:
#         preferences = UserPreferences(user_id=user_id, **movie_prefenrences.dict())
#         db.add(preferences)
#     else:
#         for key, value in movie_prefenrences.dict().items():
#             setattr(preferences, key, value)
#     db.commit()
#     db.refresh(preferences)
#     return preferences
    
# @router.post("/genres/{user_id}", response_model=UserPreferencesResponse)
# def add_genres_preferences(genre_prefenrences: UserPreferencesCreate, user_id: int, db: Session = Depends(get_db)):
#     preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
#     if not preferences:
#         preferences = UserPreferences(user_id=user_id, **genre_prefenrences.dict())
#         db.add(preferences)
#     else:
#         for key, value in genre_prefenrences.dict().items():
#             setattr(preferences, key, value)
#     db.commit()
#     db.refresh(preferences)
#     return preferences

# @router.post("/actors/{user_id}", response_model=UserPreferencesResponse)
# def add_actors_preferences(actors_prefenrences: UserPreferencesCreate, user_id: int, db: Session = Depends(get_db)):
#     preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
#     if not preferences:
#         preferences = UserPreferences(user_id=user_id, **actors_prefenrences.dict())
#         db.add(preferences)
#     else:
#         for key, value in actors_prefenrences.dict().items():
#             setattr(preferences, key, value)
#     db.commit()
#     db.refresh(preferences)
#     return preferences
    
# @router.get("/{user_id}", response_model=UserPreferencesResponse)
# def get_preferences(user_id: int, db: Session = Depends(get_db)):
#     preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
#     if not preferences:
#         raise HTTPException(status_code=404, detail="Préférences non trouvées")
#     return preferences

# @router.get("/movies/{user_id}", response_model=UserPreferencesResponse)
# def get_movies_preferences(user_id: int, db: Session = Depends(get_db)):
#     preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
#     if not preferences:
#         raise HTTPException(status_code=404, detail="Préférences non trouvées")
#     return preferences

# @router.get("/genres/{user_id}", response_model=UserPreferencesResponse)
# def get_genres_preferences(user_id: int, db: Session = Depends(get_db)):
#     preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
#     if not preferences:
#         raise HTTPException(status_code=404, detail="Préférences non trouvées")
#     return preferences

# @router.get("/actors/{user_id}", response_model=UserPreferencesResponse)
# def get_actors_preferences(user_id: int, db: Session = Depends(get_db)):
#     preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
#     if not preferences:
#         raise HTTPException(status_code=404, detail="Préférences non trouvées")
#     return preferences
