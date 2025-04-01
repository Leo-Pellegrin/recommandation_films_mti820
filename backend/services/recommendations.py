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
            posterPath=movie_dict[movie_id].poster_path,
            preferenceScore=round((score/weighted_ratings.max()) * 100,2)
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
            posterPath=movie_dict[movie_id].poster_path,
            preferenceScore=round((score / global_max) * 100, 2)
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

    movie_responses = [
        UserRecommendationResponse(
            movie_id=row.movie_id,
            title=movie_dict[row.movie_id].title,
            year=movie_dict[row.movie_id].year,
            genres=movie_dict[row.movie_id].genres,
            posterPath=movie_dict[row.movie_id].poster_path,
            preferenceScore=round((row.score / max_score)*100,2)
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
    scored_movies = []

    for movie in movies:
        if not movie.actors:
            continue
        movie_actors = set(actor.lower() for actor in movie.actors)
        common_actors = preferred_actors.intersection(movie_actors)
        match_count = len(common_actors)
        if match_count > 0:
            scored_movies.append((movie, match_count))

    if not scored_movies:
        return []

    # 3. Normaliser les scores
    max_common = max(score for _, score in scored_movies)
    scored_movies = sorted(scored_movies, key=lambda x: x[1], reverse=True)[:k]

    # 4. Construire la réponse
    movie_responses = [
        UserRecommendationResponse(
            movie_id=movie.movie_id,
            title=movie.title,
            year=movie.year,
            genres=movie.genres,
            posterPath=movie.poster_path,
            preferenceScore=round((score / max_common) * 100, 2)
        )
        for movie, score in scored_movies
    ]

    return movie_responses



# --- Filtrage hybride (User-based + Content-based + Item-based + Actor-based ) ---
def get_hybrid_recommendations(user_id: int, db: Session, k: int = 10) -> List[UserRecommendationResponse]:
    # 1. Obtenir les recommandations de chaque stratégie
    user_recs = get_collaborative_recommendations_user_based(user_id, db, k=50)
    item_recs = get_collaborative_recommendations_item_based(user_id, db, k=50)
    content_recs = get_content_based_recommendations(user_id, db, k=50)
    actors_recs = get_actor_based_recommendations(user_id, db, k=50)

    # 2. Définir les poids
    weights = {
        "user": 3,
        "item": 5,
        "content": 2,
        "actor": 2
    }

    score_dict = Counter()
    movie_info = {}

    # 3. Fonction pour intégrer une source avec normalisation
    def add_normalized_scores(recs, weight):
        if not recs:
            return
        max_score = max(r.preferenceScore for r in recs) or 1
        for r in recs:
            norm_score = r.preferenceScore / max_score  # Normalisation 0-1
            score_dict[r.movie_id] += norm_score * weight
            if r.movie_id not in movie_info:
                movie_info[r.movie_id] = r

    # 4. Ajouter chaque type de recommandations
    add_normalized_scores(user_recs, weights["user"])
    add_normalized_scores(item_recs, weights["item"])
    add_normalized_scores(content_recs, weights["content"])
    add_normalized_scores(actors_recs, weights["actor"])

    # 5. Trier les scores combinés
    top_movies = score_dict.most_common(k)
    max_total_score = max(score for _, score in top_movies) or 1
    
    # 6. Construire les réponses finales, normalisées sur 100
    hybrid_responses = [
        UserRecommendationResponse(
            movie_id=movie_info[movie_id].movie_id,
            title=movie_info[movie_id].title,
            year=movie_info[movie_id].year,
            genres=movie_info[movie_id].genres,
            posterPath=movie_info[movie_id].posterPath,
            preferenceScore=round((score / max_total_score) * 100, 2)
        )
        for movie_id, score in top_movies
    ]

    return hybrid_responses

def get_similar_movies(movie_id: int, db: Session, k: int = 10) -> List[UserRecommendationResponse]:
    # 1. Récupérer toutes les notations
    ratings = db.query(Rating).all()
    if not ratings:
        return []

    # 2. Créer la matrice utilisateur-film
    df = pd.DataFrame([{
        "user_id": r.user_id,
        "movie_id": r.movie_id,
        "rating": r.rating
    } for r in ratings])
    user_item_matrix = df.pivot_table(index="user_id", columns="movie_id", values="rating").fillna(0)

    # 3. Vérifier que le film existe
    if movie_id not in user_item_matrix.columns:
        return []

    # 4. Calculer la similarité cosinus entre les films
    item_sim_matrix = cosine_similarity(user_item_matrix.T)
    item_sim_df = pd.DataFrame(item_sim_matrix, index=user_item_matrix.columns, columns=user_item_matrix.columns)

    # 5. Récupérer les k films les plus similaires
    similar_scores = item_sim_df[movie_id].drop(labels=[movie_id])
    top_similar = similar_scores.sort_values(ascending=False).head(k)

    # 6. Récupérer les films depuis la base
    recommended_movies = db.query(Movie).filter(Movie.movie_id.in_(top_similar.index.tolist())).all()
    movie_dict = {movie.movie_id: movie for movie in recommended_movies}
    max_score = top_similar.max() or 1

    # 7. Construire les réponses
    return [
        UserRecommendationResponse(
            movie_id=movie.movie_id,
            title=movie.title,
            year=movie.year,
            genres=movie.genres,
            posterPath=movie.poster_path,
            preferenceScore=round((top_similar[movie.movie_id] / max_score) * 100, 2)
        )
        for movie in recommended_movies if movie.movie_id in top_similar.index
    ]