from sqlalchemy.orm import Session
from models import Movie, Rating
from schemas import MovieResponse
from surprise import SVD, Dataset, Reader
import pandas as pd

def convert_movies_to_response(movies):
    return [MovieResponse(
        movie_id=m.movie_id,
        title=m.title,
        year=m.year,
        genres=m.genres
    ) for m in movies]

def get_collaborative_recommendations(user_id: int, db: Session, n: int = 5):
    # écupère toutes les notations
    all_ratings = db.query(Rating).all()
    if not all_ratings:
        return []

    # Conversion en DataFrame
    df = pd.DataFrame([{
        "userId": r.user_id,
        "movieId": r.movie_id,
        "rating": r.rating
    } for r in all_ratings])

    # Dataset Surprise
    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(df[["userId", "movieId", "rating"]], reader)
    trainset = data.build_full_trainset()

    # Entraînement du modèle SVD
    model = SVD()
    model.fit(trainset)

    # Liste des films vus par l'utilisateur
    seen_movie_ids = df[df["userId"] == user_id]["movieId"].tolist()

    # Tous les films
    all_movie_ids = [m.movie_id for m in db.query(Movie.movie_id).all()]
    unseen_movie_ids = list(set(all_movie_ids) - set(seen_movie_ids))

    # Prédictions sur films non vus
    predictions = [(mid, model.predict(user_id, mid).est) for mid in unseen_movie_ids]
    predictions.sort(key=lambda x: x[1], reverse=True)
    top_movie_ids = [mid for mid, _ in predictions[:n]]

    # Récupération des films recommandés
    movies = db.query(Movie).filter(Movie.movie_id.in_(top_movie_ids)).all()
    return convert_movies_to_response(movies)
