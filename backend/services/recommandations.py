from sqlalchemy.orm import Session
from models import Movie, Rating
from schemas import MovieResponse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

# 🔹 Helper pour convertir Movie SQLAlchemy en MovieResponse
def convert_movies_to_response(movies):
    return [MovieResponse(
        movie_id=m.movie_id,
        title=m.title,
        year=m.year,
        genres=m.genres
    ) for m in movies]

# 🔹 Filtrage Collaboratif
def get_collaborative_recommendations(user_id: int, db: Session, n: int = 5):
    ratings = db.query(Rating).all()
    if not ratings:
        return []

    df = pd.DataFrame([{
        "userId": r.user_id,
        "movieId": r.movie_id,
        "rating": r.rating
    } for r in ratings])

    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(df[["userId", "movieId", "rating"]], reader)

    trainset = data.build_full_trainset()
    model = SVD()
    model.fit(trainset)

    movie_ids = db.query(Movie.movie_id).all()
    movie_ids = [m[0] for m in movie_ids]

    # Récupère les films que l'utilisateur n'a pas notés
    rated_ids = df[df["userId"] == user_id]["movieId"].tolist()
    unrated_ids = list(set(movie_ids) - set(rated_ids))

    predictions = []
    for mid in unrated_ids:
        pred = model.predict(user_id, mid)
        predictions.append((mid, pred.est))

    top_ids = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]
    movies = db.query(Movie).filter(Movie.movie_id.in_([mid for mid, _ in top_ids])).all()

    return convert_movies_to_response(movies)

# 🔹 Filtrage basé sur le contenu
def get_content_based_recommendations(user_id: int, db: Session, n: int = 5):
    ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    if not ratings:
        return []

    user_rated_movie_ids = [r.movie_id for r in ratings if r.rating >= 3.5]
    user_movies = db.query(Movie).filter(Movie.movie_id.in_(user_rated_movie_ids)).all()
    all_movies = db.query(Movie).all()

    if not user_movies or not all_movies:
        return []

    df = pd.DataFrame([{
        "movie_id": m.movie_id,
        "title": m.title,
        "genres": " ".join(m.genres)
    } for m in all_movies])

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df["genres"])

    liked_indices = df[df["movie_id"].isin(user_rated_movie_ids)].index
    similarity_scores = cosine_similarity(tfidf_matrix[liked_indices], tfidf_matrix)

    avg_sim = similarity_scores.mean(axis=0)
    top_indices = avg_sim.argsort()[::-1]

    recommended_ids = df.iloc[top_indices]["movie_id"].tolist()
    recommended_ids = [mid for mid in recommended_ids if mid not in user_rated_movie_ids][:n]

    movies = db.query(Movie).filter(Movie.movie_id.in_(recommended_ids)).all()
    return convert_movies_to_response(movies)

# 🔹 Approche Hybride simple (moyenne des scores)
def get_hybrid_recommendations(user_id: int, db: Session, n: int = 5):
    collab = get_collaborative_recommendations(user_id, db, n=50)
    content = get_content_based_recommendations(user_id, db, n=50)

    scores = {}
    for i, m in enumerate(collab):
        scores[m.movie_id] = scores.get(m.movie_id, 0) + (50 - i)

    for i, m in enumerate(content):
        scores[m.movie_id] = scores.get(m.movie_id, 0) + (50 - i)

    top_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
    movies = db.query(Movie).filter(Movie.movie_id.in_([mid for mid, _ in top_ids])).all()

    return convert_movies_to_response(movies)
