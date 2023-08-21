from enum import Enum
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from api_models import Movie, MovieScore
from database import SessionLocal, get_all_movies as get_all_movies_from_database, get_movie_by_id as get_movie_by_id_from_database, get_movie_by_name as get_movie_by_name_from_database, add_movie as add_movie_to_database, add_like_to_movie as add_like_to_movie_in_database, add_dislike_to_movie as add_dislike_to_movie_in_database


app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "I am Berikoba. Welcome!"}


@app.get("/movies")
async def get_all_movies(db: Session = Depends(get_db)) -> list:
    movies_names = [movie.name for movie in get_all_movies_from_database(db)]
    return movies_names


@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int, db: Session = Depends(get_db)) -> Movie:
    movie = get_movie_by_id_from_database(db, movie_id)
    
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Movie with id: {movie_id} not found.")
    
    return movie


@app.post("/movies")
async def add_movie(movie: Movie, db: Session = Depends(get_db)) -> Movie:    
    return get_movie_by_id_from_database(db, movie)


@app.post("/movies/{movie_id}/score")
async def add_movie_score(movie_id: int, user_score: MovieScore, db: Session = Depends(get_db)) -> dict:
    movie = get_movie_by_id_from_database(db, movie_id)

    if movie is None:
        raise HTTPException(status_code=400, detail=f"Bad Request Error. Movie with id: {movie_id} is not found in movie database.")
    
    if user_score is MovieScore.like:
        add_like_to_movie_in_database(db, movie_id)
    
    if user_score is MovieScore.dislike:
        add_dislike_to_movie_in_database(db, movie_id)

    return {
        "movie_id": movie_id,
        "score": user_score,
        "likes": movie.likes,
        "dislikes": movie.dislikes,
    }
