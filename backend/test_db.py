from sqlalchemy.orm import Session
from database import get_db
from models import Movie

# Vérifier la connexion
def test_connection():
    db: Session = next(get_db())  # Ouvre une session
    movie = db.query(Movie).first()  # Récupère un film
    db.close()
    if movie:
        print(f"✅ Connexion OK ! Premier film : {movie.title}")
    else:
        print("⚠️ Connexion OK mais aucune donnée trouvée.")

test_connection()