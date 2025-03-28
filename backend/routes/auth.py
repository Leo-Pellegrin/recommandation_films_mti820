from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse
from utils.auth import hash_password, verify_password, create_access_token, get_current_user
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# 🔹 Inscription d'un utilisateur
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username.strip(), 
        email=user.email.strip(),
        password_hash=hashed_password,
        first_login=True
    )    
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"id": new_user.user_id, "username": new_user.username, "email": new_user.email, "first_login": new_user.first_login} 

# 🔹 Connexion d'un utilisateur (génération d'un token JWT)
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect")

    # Vérifier si c'est la première connexion
    first_login = user.first_login

    # Mettre `first_login = False` en base de données après connexion
    if user.first_login:
        user.first_login = False
        db.commit()

    access_token = create_access_token(data={"sub": str(user.user_id)}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer", "id": user.user_id, "username": user.username, "email": user.email, "first_login": first_login}

# 🔹 Récupérer les infos de l'utilisateur connecté
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.user_id, "username": current_user.username, "email": current_user.email} 