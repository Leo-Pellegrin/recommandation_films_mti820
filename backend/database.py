from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔹 Connexion PostgreSQL (remplace avec tes infos)
DATABASE_URL = "postgresql://postgres:@localhost:5433/movie_recommendation"

# 🔹 Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# 🔹 Gestion des sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 Déclaration de la base (CORRECTION)
Base = declarative_base()

# 🔹 Dépendance pour récupérer une session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 