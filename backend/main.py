from fastapi import FastAPI
from routes import auth, movies, users, ratings, links, preferences
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(movies.router, prefix="/api/movies", tags=["Movies"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(ratings.router, prefix="/api/ratings", tags=["Ratings"])
app.include_router(links.router, prefix="/api/links", tags=["Links"])
# app.include_router(preferences.router, prefix="/api/preferences", tags=["Preferences"])

@app.get("/")
def root():
    return {"message": "🚀 API de recommandations de films en ligne !"}