from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT
from database import Base

# class UserPreferences(Base):
#     __tablename__ = "user_preferences"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), unique=True)
#     favorite_genres = Column(String, nullable=True)  # Ex: "Action, Drame, Science-Fiction"
#     favorite_actors = Column(String, nullable=True)  # Ex: "Leonardo DiCaprio, Brad Pitt"

#     user = relationship("User", back_populates="preferences")
    
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=True)
    first_login = Column(Boolean, nullable=True)

    # preferences = relationship("UserPreferences", back_populates="user", uselist=False)

class UserFeature(Base):
    __tablename__ = "user_features"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, index=True)
    preferred_genres = Column(ARRAY(TEXT), index=True)
    avg_rating_given = Column(Float, index=True)
    num_ratings = Column(Integer, index=True)

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    year = Column(Integer, index=True)
    genres = Column(ARRAY(TEXT), index=True)
    
class MovieFeature(Base):
    __tablename__ = "movie_features"

    movie_id = Column(Integer, ForeignKey("movies.movie_id"), primary_key=True, index=True)
    embedding_vector = Column(ARRAY(Float), index=True)
    genre_embedding = Column(ARRAY(Float), index=True)
    popularity = Column(Float, index=True)

class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    rating = Column(Integer, index=True)
    timestamp = Column(DateTime, index=True)

class Link(Base):
    __tablename__ = "links"

    movie_id = Column(Integer, ForeignKey("movies.movie_id"), primary_key=True, index=True)
    imdb_id = Column(Integer, index=True)
    tmdb_id = Column(Integer, index=True)
    
class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    tag = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    
class Recommendation(Base):
    __tablename__ = "recommendations"
    
    rec_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    score = Column(Integer, index=True)
    

    