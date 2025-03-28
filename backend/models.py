from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT
from database import Base
from datetime import datetime  

    
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=True)
    first_login = Column(Boolean, nullable=True)

    favorite_movies = relationship("UserMoviePreference", back_populates="user", cascade="all, delete")
    preferences = relationship("Preference", back_populates="user", uselist=False)

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
    poster_path = Column(String) 

    
    link = relationship("Link", back_populates="movie", uselist=False)
    
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
    
    movie = relationship("Movie", back_populates="link")

    
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
    
class UserMoviePreference(Base):
    __tablename__ = "user_movie_preferences"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), primary_key=True)
    rating = Column(Integer, index=True)

    user = relationship("User", back_populates="favorite_movies")
    movie = relationship("Movie")

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False)

    preferred_genres = Column(ARRAY(String), default=[])
    preferred_actors = Column(ARRAY(String), default=[])

    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="preferences")
    