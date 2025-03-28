import sys
import os
import random

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
    
# def test_update_preferences():
#     response = client.post("/api/preferences", json={
#         "user_id": 1,
#         "favorite_genres": ["Action", "Sci-Fi"]
#     })
#     assert response.status_code == 200
#     assert "favorite_genres" in response.json()

# def test_get_preferences():
#     response = client.get("/api/preferences/1")
#     assert response.status_code == 200
#     assert isinstance(response.json()["favorite_genres"], list)