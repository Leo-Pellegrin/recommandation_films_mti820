from surprise import Dataset, Reader, KNNBasic
from sqlalchemy.orm import Session
from models import Rating, Movie
from schemas import MovieResponse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Filtrage collaboratif user-based ---
def get_collaborative_recommendations_user_based(user_id: int, db: Session, k: int = 5) -> list[MovieResponse]:
    # 1. Récupérer toutes les notations depuis la base de données
    ratings = db.query(Rating).all()
    if not ratings:
        return []

    # 2. Convertir les notations en DataFrame pour Surprise
    data_dict = {
        "userID": [str(r.user_id) for r in ratings],
        "itemID": [str(r.movie_id) for r in ratings],
        "rating": [r.rating for r in ratings]
    }
    df = pd.DataFrame(data_dict)

    # 3. Charger les données avec Surprise
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(df[["userID", "itemID", "rating"]], reader)
    trainset = data.build_full_trainset()

    # 4. Entraîner le modèle KNN user-based
    sim_options = {
        "name": "cosine",
        "user_based": True
    }
    algo = KNNBasic(sim_options=sim_options)
    algo.fit(trainset)

    # 5. Identifier les films non notés par l'utilisateur
    all_movie_ids = set(str(r.movie_id) for r in ratings)
    user_movie_ids = set(str(r.movie_id) for r in ratings if r.user_id == user_id)
    movies_to_predict = all_movie_ids - user_movie_ids

    # 6. Prédire les notes pour ces films
    predictions = []
    for movie_id in movies_to_predict:
        pred = algo.predict(str(user_id), movie_id)
        predictions.append((int(movie_id), pred.est))

    # 7. Trier par note prédite
    top_predictions = sorted(predictions, key=lambda x: x[1], reverse=True)[:k]

    # 8. Récupérer les films correspondants depuis la base
    recommended_movies = (
        db.query(Movie)
        .filter(Movie.movie_id.in_([movie_id for movie_id, _ in top_predictions]))
        .all()
    )

    # 9. Convertir en schéma de réponse
    movie_responses = [
        MovieResponse(
            movie_id=movie.movie_id,
            title=movie.title,
            year=movie.year,
            genres=movie.genres
        ) for movie in recommended_movies
    ]

    return movie_responses


# --- Filtrage collaboratif item-based ---
def get_collaborative_recommendations_item_based(user_id: int, db: Session, k: int = 5) -> list[MovieResponse]:
    # 1. Récupérer toutes les notations depuis la base de données
    ratings = db.query(Rating).all()
    if not ratings:
        return []

    # 2. Convertir les notations en DataFrame pour Surprise
    data_dict = {
        "userID": [str(r.user_id) for r in ratings],
        "itemID": [str(r.movie_id) for r in ratings],
        "rating": [r.rating for r in ratings]
    }
    df = pd.DataFrame(data_dict)

    # 3. Charger les données avec Surprise
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(df[["userID", "itemID", "rating"]], reader)
    trainset = data.build_full_trainset()

    # 4. Entraîner le modèle KNN item-based
    sim_options = {
        "name": "cosine",
        "user_based": False
    }
    algo = KNNBasic(sim_options=sim_options)
    algo.fit(trainset)

    # 5. Identifier les films non notés par l'utilisateur
    all_movie_ids = set(str(r.movie_id) for r in ratings)
    user_movie_ids = set(str(r.movie_id) for r in ratings if r.user_id == user_id)
    movies_to_predict = all_movie_ids - user_movie_ids

    # 6. Prédire les notes pour ces films
    predictions = []
    for movie_id in movies_to_predict:
        pred = algo.predict(str(user_id), movie_id)
        predictions.append((int(movie_id), pred.est))

    # 7. Trier par note prédite
    top_predictions = sorted(predictions, key=lambda x: x[1], reverse=True)[:k]

    # 8. Récupérer les films correspondants depuis la base
    recommended_movies = (
        db.query(Movie)
        .filter(Movie.movie_id.in_([movie_id for movie_id, _ in top_predictions]))
        .all()
    )

    # 9. Convertir en schéma de réponse
    movie_responses = [
        MovieResponse(
            movie_id=movie.movie_id,
            title=movie.title,
            year=movie.year,
            genres=movie.genres
        ) for movie in recommended_movies
    ]

    return movie_responses


# --- Filtrage basé sur le contenu ---
def get_content_based_recommendations(user_id: int, db: Session, k: int = 5) -> list[MovieResponse]:
    # 1. Récupérer tous les films et préférences de l'utilisateur
    movies = db.query(Movie).all()
    ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    if not movies or not ratings:
        return []

    # 2. Créer un DataFrame des films
    df_movies = pd.DataFrame([{
        "movie_id": movie.movie_id,
        "title": movie.title,
        "genres": " ".join(movie.genres) if movie.genres else ""
    } for movie in movies])

    # 3. Appliquer le TF-IDF sur les genres (peut être remplacé par embeddings plus tard)
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df_movies["genres"])

    # 4. Calculer la similarité cosinus entre tous les films
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 5. Identifier les films déjà notés
    watched_movie_ids = [r.movie_id for r in ratings]
    watched_indices = df_movies[df_movies.movie_id.isin(watched_movie_ids)].index

    # 6. Calculer les scores de similarité globaux
    similarity_scores = cosine_sim[watched_indices].mean(axis=0)

    # 7. Sélectionner les meilleurs films non vus
    df_movies["score"] = similarity_scores
    recommendations = df_movies[~df_movies.movie_id.isin(watched_movie_ids)].sort_values("score", ascending=False).head(k)

    # 8. Récupérer les films recommandés depuis la base
    recommended_movies = db.query(Movie).filter(Movie.movie_id.in_(recommendations.movie_id.tolist())).all()

    # 9. Convertir en MovieResponse
    movie_responses = [
        MovieResponse(
            movie_id=movie.movie_id,
            title=movie.title,
            year=movie.year,
            genres=movie.genres
        ) for movie in recommended_movies
    ]

    return movie_responses