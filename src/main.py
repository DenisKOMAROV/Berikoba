from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Movie(BaseModel):
    name: str


app = FastAPI()

db = {
    0: "Lord of the Rings",
}

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/extra")
async def root():
    return {"message": "Hello World Extra"}


@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int) -> str:
    movie = db.get(movie_id, None)
    
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Movie {movie_id} not found")
    
    return movie


@app.post("/movies/{movie_id}")
async def add_movie(movie_id:int, movie: Movie):
    if movie_id in db.keys():
        raise HTTPException(status_code=400, detail=f"Bad Request Error. Movie with id: {movie_id} already exists.")
    
    db[movie_id] = movie.name
