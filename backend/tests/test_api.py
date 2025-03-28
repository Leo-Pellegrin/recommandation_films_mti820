import sys
import os
import random
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)  # Client de test

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "🚀 API de recommandations de films en ligne !"}

def test_register():
    random_username = f"test_user_{random.randint(1000, 9999)}"  
    random_email = f"test{random.randint(1000, 9999)}@example.com"
    response = client.post("/api/auth/register", json={
        "username": random_username,
        "email": random_email,
        "password": "testpassword"
    })
    
    print(response.json())  
    assert response.status_code == 200
    assert "id" in response.json()
    return response.json()["id"]

def test_get_user_by_id():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_login():
    response = client.post("/api/auth/login", data={
        "username": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    global ACCESS_TOKEN  
    ACCESS_TOKEN = json_data["access_token"]
    

def test_get_me():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    assert "email" in response.json()

def test_add_movie():
    response = client.post("/api/movies", json={
        "title": "Inception",
        "year": 2010,
        "genres": ["Sci-Fi", "Thriller"]
    })
    
    print(response.json()) 
    assert response.status_code == 200
    assert "movie_id" in response.json(), "La réponse ne contient pas 'movie_id'"
    
    return response.json()["movie_id"]  

def test_get_movies():
    response = client.get("/api/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movie():
    response = client.get("/api/movies/1")
    assert response.status_code == 200
    assert "title" in response.json()

def test_add_rating():
    response = client.post("/api/ratings", json={
        "user_id": 1,
        "movie_id": 1,
        "rating": 4.5
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_user_ratings():
    response = client.get("/api/ratings/user/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_average_rating():
    response = client.get("/api/ratings/movie/1/average")
    assert response.status_code == 200
    assert "average_rating" in response.json()

def test_add_link():
    movie_id = test_add_movie()
    
    response = client.post("/api/links", json={
        "movie_id": movie_id,
        "imdb_id": 123456,
        "tmdb_id": 654321
    })
    assert response.status_code == 200
    assert response.json()["imdb_id"] == 123456

def test_get_link():
    response = client.get("/api/links/1")
    assert response.status_code == 200
    assert "imdb_id" in response.json()
    
@pytest.fixture
def test_user_id():
    return 1

@pytest.fixture
def test_movie_ids():
    return [101, 102, 103]    
 
# -------------------------
# 📌 TESTS GENRES
# -------------------------

def test_set_genres(test_user_id):
    res = client.post(f"/users/{test_user_id}/preferences/genres", json={"genres": ["Action", "Thriller"]})
    assert res.status_code == 200
    assert "updated" in res.json()["message"]

def test_get_genres(test_user_id):
    res = client.get(f"/users/{test_user_id}/preferences/genres")
    assert res.status_code == 200
    assert "preferred_genres" in res.json()

def test_delete_one_genre(test_user_id):
    res = client.delete(f"/users/{test_user_id}/preferences/genres/Thriller")
    assert res.status_code == 200
    assert "removed" in res.json()["message"]

# -------------------------
# 📌 TESTS ACTORS
# -------------------------

def test_set_actors(test_user_id):
    res = client.post(f"/users/{test_user_id}/preferences/actors", json={"actors": ["Ryan Gosling", "Scarlett Johansson"]})
    assert res.status_code == 200

def test_get_actors(test_user_id):
    res = client.get(f"/users/{test_user_id}/preferences/actors")
    assert res.status_code == 200
    assert "preferred_actors" in res.json()

def test_delete_one_actor(test_user_id):
    res = client.delete(f"/users/{test_user_id}/preferences/actors/Ryan Gosling")
    assert res.status_code == 200

# -------------------------
# 📌 TESTS FILMS FAVORIS
# -------------------------

def test_add_favorite_movies_batch(test_user_id, test_movie_ids):
    res = client.post(f"/users/{test_user_id}/favorites/movies/batch", json={"movie_ids": test_movie_ids})
    assert res.status_code == 200

def test_get_favorite_movies(test_user_id):
    res = client.get(f"/users/{test_user_id}/favorites/movies")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_delete_one_favorite_movie(test_user_id):
    res = client.delete(f"/users/{test_user_id}/favorites/movies/101")
    assert res.status_code == 200

def test_delete_multiple_favorite_movies(test_user_id):
    res = client.delete(f"/users/{test_user_id}/favorites/movies/batch", json={"movie_ids": [102, 103]})
    assert res.status_code == 200