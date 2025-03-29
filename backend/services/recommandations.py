# --- Imports nécessaires ---
from sqlalchemy.orm import Session
from models import Rating, Movie, Preference
from schemas import UserRecommendationResponse
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List
from collections import Counter


# --- Filtrage collaboratif user-based (similarité cosinus) ---
def get_collaborative_recommendations_user_based(user_id: int, db: Session, k: int = 5) -> List[UserRecommendationResponse]:
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
    movie_dict = {movie.movie_id: movie for movie in recommended_movies}
    
    

    # 9. Trier les recommandations et construire les réponses avec score normalisé 
    sorted_recommendations = recommendations.sort_values(ascending=False)
    movie_responses = [
        UserRecommendationResponse(
            movie_id=movie_dict[movie_id].movie_id,
            title=movie_dict[movie_id].title,
            year=movie_dict[movie_id].year,
            genres=movie_dict[movie_id].genres,
            poster_path=movie_dict[movie_id].poster_path,
            preference_score=(score/weighted_ratings.max()) * 100
        )
        for movie_id, score in sorted_recommendations.items()
        if movie_id in movie_dict
    ]

    return movie_responses

# --- Filtrage collaboratif item-based (similarité cosinus) ---
def get_collaborative_recommendations_item_based(user_id: int, db: Session, k: int = 5) -> List[UserRecommendationResponse]:
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

    # 4. Calculer la similarité cosinus entre films
    item_sim_matrix = cosine_similarity(user_item_matrix.T)
    item_sim_df = pd.DataFrame(item_sim_matrix, index=user_item_matrix.columns, columns=user_item_matrix.columns)

    # 5. Récupérer les films notés par l'utilisateur
    watched_movie_ids = user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index.tolist()
    if not watched_movie_ids:
        return []

    # 6. Calculer les scores de similarité moyens avec les films vus
    sim_scores = item_sim_df[watched_movie_ids].mean(axis=1)

    # 7. Exclure les films déjà vus et trier
    unseen_movies = sim_scores.index.difference(watched_movie_ids)
    top_recommendations = sim_scores.loc[unseen_movies].sort_values(ascending=False).head(k)

    # 8. Récupérer les films recommandés depuis la base
    recommended_movies = db.query(Movie).filter(Movie.movie_id.in_(top_recommendations.index.tolist())).all()
    movie_dict = {movie.movie_id: movie for movie in recommended_movies}

    # 9. Convertir en UserRecommendationResponse trié, avec score normalisé
    global_max = sim_scores.max()
    movie_responses = [
        UserRecommendationResponse(
            movie_id=movie_dict[movie_id].movie_id,
            title=movie_dict[movie_id].title,
            year=movie_dict[movie_id].year,
            genres=movie_dict[movie_id].genres,
            poster_path=movie_dict[movie_id].poster_path,
            preference_score=round((score / global_max) * 100, 2)
        )
        for movie_id, score in top_recommendations.items()
        if movie_id in movie_dict
    ]

    return movie_responses


# --- Filtrage basé sur les genres préférés (TF-IDF) ---
def get_content_based_recommendations(user_id: int, db: Session, k: int = 5) -> List[UserRecommendationResponse]:
    # 1. Récupérer les films et les préférences de l'utilisateur
    movies = db.query(Movie).all()
    preferences = db.query(Preference).filter(Preference.user_id == user_id).first()
    if not movies or not preferences or not preferences.preferred_genres:
        return []

    preferred_genres = set(g.lower() for g in preferences.preferred_genres)

    # 2. Créer un DataFrame des films avec leurs genres
    df_movies = pd.DataFrame([{
        "movie_id": movie.movie_id,
        "title": movie.title,
        "genres": " ".join(movie.genres) if movie.genres else ""
    } for movie in movies])

    # 3. Appliquer le TF-IDF sur les genres
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df_movies["genres"])

    # 4. Créer un vecteur binaire représentant les genres préférés de l'utilisateur
    user_genre_vector = tfidf.transform([" ".join(preferred_genres)])
    print(user_genre_vector)

    # 5. Calculer la similarité cosinus entre l'utilisateur et tous les films
    similarity_scores = cosine_similarity(user_genre_vector, tfidf_matrix).flatten()

    # 6. Ajouter les scores au DataFrame
    df_movies["score"] = similarity_scores

    # 7. Trier et récupérer les meilleurs films
    top_recommendations = df_movies.sort_values("score", ascending=False).head(k)

    # 8. Récupérer les films depuis la base
    recommended_movies = db.query(Movie).filter(Movie.movie_id.in_(top_recommendations.movie_id.tolist())).all()
    movie_dict = {movie.movie_id: movie for movie in recommended_movies}
    max_score = top_recommendations["score"].max()

    # 9. Convertir en UserRecommendationResponse
    if not max_score or pd.isna(max_score) or max_score == 0:
        max_score = 1

    movie_responses = [
        UserRecommendationResponse(
            movie_id=row.movie_id,
            title=movie_dict[row.movie_id].title,
            year=movie_dict[row.movie_id].year,
            genres=movie_dict[row.movie_id].genres,
            poster_path=movie_dict[row.movie_id].poster_path,
            preference_score=row.score / max_score
        )
        for row in top_recommendations.itertuples()
        if row.movie_id in movie_dict
    ]

    return movie_responses


# --- Filtrage basé sur les acteurs préférés ---
def get_actor_based_recommendations(user_id: int, db: Session, k: int = 5) -> List[UserRecommendationResponse]:
    # 1. Récupérer les préférences de l'utilisateur
    preferences = db.query(Preference).filter(Preference.user_id == user_id).first()
    if not preferences or not preferences.preferred_actors:
        return []

    preferred_actors = set(actor.lower() for actor in preferences.preferred_actors)

    # 2. Récupérer les films avec des acteurs
    movies = db.query(Movie).all()
    movie_scores = []

    for movie in movies:
        if not movie.actors:
            continue
        movie_actors = set(actor.lower() for actor in movie.actors)
        common_actors = preferred_actors.intersection(movie_actors)
        if common_actors:
            score = round(len(common_actors) / len(preferred_actors) * 100, 2)
            movie_scores.append((movie, score))

    # 3. Trier les films selon le score de correspondance
    top_matches = sorted(movie_scores, key=lambda x: x[1], reverse=True)[:k]

    # 4. Construire les réponses
    movie_responses = [
        UserRecommendationResponse(
            movie_id=movie.movie_id,
            title=movie.title,
            year=movie.year,
            genres=movie.genres,
            poster_path=movie.poster_path,
            preference_score=score
        )
        for movie, score in top_matches
    ]

    return movie_responses



# --- Filtrage hybride (User-based + Content-based + Item-based si souhaité) ---
def get_hybrid_recommendations(user_id: int, db: Session, k: int = 10) -> List[UserRecommendationResponse]:
    # 1. Obtenir les recommandations de chaque stratégie (top 50 pour couvrir plus large)
    user_recs = get_collaborative_recommendations_user_based(user_id, db, k=50)
    item_recs = get_collaborative_recommendations_item_based(user_id, db, k=50)
    content_recs = get_content_based_recommendations(user_id, db, k=50)

    # 2. Créer un dictionnaire de score combiné
    score_dict = Counter()
    movie_info = {}

    for rec in user_recs:
        score_dict[rec.movie_id] += rec.preference_score * 5  # Poids pour user-based
        movie_info[rec.movie_id] = rec

    for rec in item_recs:
        score_dict[rec.movie_id] += rec.preference_score * 3  # Poids pour item-based
        movie_info[rec.movie_id] = rec

    for rec in content_recs:
        score_dict[rec.movie_id] += rec.preference_score * 2  # Poids pour content-based
        movie_info[rec.movie_id] = rec

    # 3. Trier les films par score total
    top_movies = score_dict.most_common(k)

    # 4. Retourner les UserRecommendationResponse triés
    hybrid_responses = [
        UserRecommendationResponse(
            movie_id=movie_info[movie_id].movie_id,
            title=movie_info[movie_id].title,
            year=movie_info[movie_id].year,
            genres=movie_info[movie_id].genres,
            poster_path=movie_info[movie_id].poster_path,
            preference_score=round(score, 2)
        )
        for movie_id, score in top_movies
    ]

    return hybrid_responses
