from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class MovieBase(BaseModel):
    title: str
    year: int
    genres: List[str]  
    poster_path: Optional[str] = None

class MovieCreate(MovieBase):
    pass  # Aucun champ supplémentaire

class MovieResponse(MovieBase):
    movie_id: int
    model_config = ConfigDict(from_attributes=True)
        
class UserCreate(BaseModel):
    username: str
    email: str
    password: str  

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
    model_config = ConfigDict(from_attributes=True)

class RatingCreate(BaseModel):
    movie_id: int
    rating: int
    timestamp: Optional[datetime] = None

class RatingResponse(RatingCreate):
    id: int    
    model_config = ConfigDict(from_attributes=True)

class LinkCreate(BaseModel):
    movie_id: int
    imdb_id: int
    tmdb_id: int

class LinkResponse(LinkCreate):
    model_config = ConfigDict(from_attributes=True)

        
class UserPreferencesCreate(BaseModel):
    user_id: int
    favorite_genres: List[str]

class UserPreferencesResponse(UserPreferencesCreate):
    model_config = ConfigDict(from_attributes=True)

class GenresResponse(BaseModel):
    genre: str
    model_config = ConfigDict(from_attributes=True)
    
class GenreList(BaseModel):
    genres: List[str]

class ActorList(BaseModel):
    actors: List[str]

class MovieIDList(BaseModel):
    movie_ids: List[int]

class UserRecommendationResponse(BaseModel):
    movie_id: int
    title: str
    year: int
    genres: List[str]
    poster_path: str | None = None  
    preference_score: float  

    model_config = ConfigDict(from_attributes=True)