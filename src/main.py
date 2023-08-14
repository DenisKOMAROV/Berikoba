from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class Movie(BaseModel):
    name: str


app = FastAPI()

db = {
    0: Movie(name = "Lord of the Rings"),
    1: Movie(name = "Hobbit"),    
}

@app.get("/")
async def root():
    return {"message": "I am Berikoba. Welcome!"}


@app.get("/movies")
async def get_all_movies():
    return jsonable_encoder(list(db.values()))

@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int) -> Movie:
    movie = db.get(movie_id, None)
    
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Movie with id: {movie_id} not found.")
    
    return movie


@app.post("/movies/{movie_id}")
async def add_movie(movie_id:int, movie: Movie):
    if movie_id in db.keys():
        raise HTTPException(status_code=400, detail=f"Bad Request Error. Movie with id: {movie_id} already exists.")
    
    db[movie_id] = movie
