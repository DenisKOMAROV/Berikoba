from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class Movie(BaseModel):
    """
    A class representing a movie.

    Attributes
    ----------
    name : str
        The name of the movie.
    likes : int, optional
        The number of likes the movie has received. Default is 0.
    dislikes : int, optional
        The number of dislikes the movie has received. Default is 0.
    """
    name: str           # Movie name
    likes: int = 0      # Add a likes counter
    dislikes: int = 0   # Add a dislikes counter


class MovieScore(str, Enum):
    like = "like"
    dislike = "dislike"


app = FastAPI()

db = {
    0: Movie(name = "Lord of the Rings"),
    1: Movie(name = "Hobbit"),    
}


@app.get("/")
async def root():
    return {"message": "I am Berikoba. Welcome!"}


@app.get("/movies")
async def get_all_movies() -> list:
    movies_names = [movie.name for movie in db.values()]
    return movies_names

@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int) -> Movie:
    movie = db.get(movie_id, None)
    
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Movie with id: {movie_id} not found.")
    
    return movie


@app.post("/movies/{movie_id}")
async def add_movie(movie_id:int, movie: Movie) -> None:
    if movie_id in db.keys():
        raise HTTPException(status_code=400, detail=f"Bad Request Error. Movie with id: {movie_id} already exists.")
    
    db[movie_id] = movie


@app.post("/movies/{movie_id}/score")
async def add_movie_score(movie_id: int, user_score: MovieScore) -> dict:
    movie = db.get(movie_id, None)

    if movie is None:
        raise HTTPException(status_code=400, detail=f"Bad Request Error. Movie with id: {movie_id} is not found in movie database.")
    
    if user_score is MovieScore.like:
        movie.likes += 1
    
    if user_score is MovieScore.dislike:
        movie.dislikes += 1

    return {
        "movie_id": movie_id,
        "score": user_score,
        "likes": movie.likes,
        "dislikes": movie.dislikes,
    }
