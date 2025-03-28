# --- Imports nécessaires ---
from sqlalchemy.orm import Session
from models import Rating, Movie
from schemas import MovieResponse
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List
from collections import Counter


# --- Filtrage collaboratif user-based (similarité cosinus) ---
def get_collaborative_recommendations_user_based(user_id: int, db: Session, k: int = 5) -> List[MovieResponse]:
    # 1. Récupérer toutes les notations depuis la base de données
    ratings = db.query(Rating).all()
    if not ratings:
        return []

    # 2. Construire un DataFrame utilisateur-film
    df = pd.DataFrame([{
        "user_id": r.user_id,
        "movie_id": r.movie_id,
        "rating": r.rating
    } for r in ratings])
    user_item_matrix = df.pivot_table(index="user_id", columns="movie_id", values="rating").fillna(0)

    # 3. Vérifier que l'utilisateur existe dans la matrice
    if user_id not in user_item_matrix.index:
        return []

    # 4. Calculer la similarité cosinus entre utilisateurs
    user_sim_matrix = cosine_similarity(user_item_matrix)
    user_sim_df = pd.DataFrame(user_sim_matrix, index=user_item_matrix.index, columns=user_item_matrix.index)

    # 5. Récupérer les similarités de l'utilisateur cible avec les autres
    sim_scores = user_sim_df.loc[user_id]

    # 6. Pondérer les notes des autres utilisateurs par leur similarité
    weighted_ratings = user_item_matrix.T.dot(sim_scores).divide(sim_scores.sum())

    # 7. Exclure les films déjà notés par l'utilisateur
    already_rated = user_item_matrix.loc[user_id]
    unrated_movies = already_rated[already_rated == 0].index
    recommendations = weighted_ratings.loc[unrated_movies].sort_values(ascending=False).head(k)

    # 8. Récupérer les films recommandés depuis la base
    recommended_movies = db.query(Movie).filter(Movie.movie_id.in_(recommendations.index.tolist())).all()

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

# --- Filtrage collaboratif item-based (similarité cosinus) ---
def get_collaborative_recommendations_item_based(user_id: int, db: Session, k: int = 5) -> List[MovieResponse]:
    # 1. Récupérer toutes les notations depuis la base de données
    ratings = db.query(Rating).all()
    if not ratings:
        return []

    # 2. Construire un DataFrame utilisateur-film
    df = pd.DataFrame([{
        "user_id": r.user_id,
        "movie_id": r.movie_id,
        "rating": r.rating
    } for r in ratings])
    user_item_matrix = df.pivot_table(index="user_id", columns="movie_id", values="rating").fillna(0)

    # 3. Vérifier que l'utilisateur existe dans la matrice
    if user_id not in user_item_matrix.index:
        return []

    # 4. Calculer la similarité cosinus entre les films (colonnes)
    item_sim_matrix = cosine_similarity(user_item_matrix.T)
    item_sim_df = pd.DataFrame(item_sim_matrix, index=user_item_matrix.columns, columns=user_item_matrix.columns)

    # 5. Récupérer les films notés par l'utilisateur
    user_ratings = user_item_matrix.loc[user_id]
    rated_movies = user_ratings[user_ratings > 0]

    # 6. Calculer les scores pondérés pour les autres films
    scores = pd.Series(0, index=user_item_matrix.columns, dtype=float)
    for movie_id, rating in rated_movies.items():
        similarities = item_sim_df[movie_id]
        scores += similarities * rating

    # 7. Normaliser les scores (optionnel mais recommandé)
    norm_factors = item_sim_df[rated_movies.index].sum(axis=1)
    scores = scores / norm_factors.replace(0, 1)

    # 8. Enlever les films déjà notés par l'utilisateur
    scores = scores.drop(labels=rated_movies.index)
    top_recommendations = scores.sort_values(ascending=False).head(k)

    # 9. Récupérer les films recommandés depuis la base
    recommended_movies = db.query(Movie).filter(Movie.movie_id.in_(top_recommendations.index.tolist())).all()

    # 10. Convertir en MovieResponse
    movie_responses = [
        MovieResponse(
            movie_id=movie.movie_id,
            title=movie.title,
            year=movie.year,
            genres=movie.genres
        ) for movie in recommended_movies
    ]

    return movie_responses

# --- Filtrage basé sur le contenu (TF-IDF sur les genres) ---
def get_content_based_recommendations(user_id: int, db: Session, k: int = 5) -> List[MovieResponse]:
    # 1. Récupérer tous les films et les notations de l'utilisateur
    movies = db.query(Movie).all()
    ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    if not movies or not ratings:
        return []

    # 2. Créer un DataFrame des films avec leurs genres
    df_movies = pd.DataFrame([{
        "movie_id": movie.movie_id,
        "title": movie.title,
        "genres": " ".join(movie.genres) if movie.genres else ""
    } for movie in movies])

    # 3. Appliquer le TF-IDF sur les genres
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df_movies["genres"])

    # 4. Calculer la similarité cosinus entre les films
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 5. Identifier les films notés par l'utilisateur
    watched_movie_ids = [r.movie_id for r in ratings]
    if not watched_movie_ids:
        return []

    watched_indices = df_movies[df_movies.movie_id.isin(watched_movie_ids)].index

    # 6. Calculer les scores de similarité moyens avec les films vus
    similarity_scores = cosine_sim[watched_indices].mean(axis=0)

    # 7. Ajouter les scores de similarité au DataFrame
    df_movies["score"] = similarity_scores

    # 8. Exclure les films déjà vus et trier
    unseen_movies = df_movies[~df_movies.movie_id.isin(watched_movie_ids)]
    top_recommendations = unseen_movies.sort_values("score", ascending=False).head(k)

    # 9. Récupérer les films depuis la base
    recommended_movies = db.query(Movie).filter(Movie.movie_id.in_(top_recommendations.movie_id.tolist())).all()

    # 10. Convertir en MovieResponse
    movie_responses = [
        MovieResponse(
            movie_id=movie.movie_id,
            title=movie.title,
            year=movie.year,
            genres=movie.genres
        ) for movie in recommended_movies
    ]

    return movie_responses

# --- Filtrage hybride (User-based + Content-based + Item-based si souhaité) ---
def get_hybrid_recommendations(user_id: int, db: Session, k: int = 10) -> List[MovieResponse]:
    # 1. Obtenir les recommandations des différentes approches
    user_based_recs = get_collaborative_recommendations_user_based(user_id, db, k=50)
    content_based_recs = get_content_based_recommendations(user_id, db, k=50)

    # 2. Pondérer et fusionner les recommandations
    score_counter = Counter()

    for movie in user_based_recs:
        score_counter[movie.movie_id] += 3  # Poids élevé : user-based
    for movie in content_based_recs:
        score_counter[movie.movie_id] += 2  # Poids moyen : content-based

    # 3. Récupérer les k meilleurs films par score total
    top_movie_ids = [movie_id for movie_id, _ in score_counter.most_common(k)]

    # 4. Récupérer les films depuis la base
    recommended_movies = db.query(Movie).filter(Movie.movie_id.in_(top_movie_ids)).all()

    # 5. Convertir en MovieResponse
    movie_responses = [
        MovieResponse(
            movie_id=movie.movie_id,
            title=movie.title,
            year=movie.year,
            genres=movie.genres
        ) for movie in recommended_movies
    ]

    return movie_responses
