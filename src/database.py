from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String
from api_models import Movie


DATABASE_URL = "postgresql://postgres:postgres@localhost/berikoba"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

class MovieModel(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    likes = Column(Integer)
    dislikes = Column(Integer)


def get_all_movies(db: Session):
    return db.query(MovieModel).all()


def get_movie_by_id(db: Session, movie_id: int):
    return db.query(MovieModel).filter(MovieModel.id == movie_id).first()


def get_movie_by_name(db: Session, movie_name: String):
    return db.query(MovieModel).filter(MovieModel.name == movie_name).first()


def add_movie(db: Session, movie: Movie):
    movie_model = MovieModel(name=movie.name, likes=0, dislikes=0)
    db.add(movie_model)
    db.commit()
    db.refresh(movie_model)
    return movie_model


def add_like_to_movie(db: Session, movie_id: int):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    
    if movie:
        setattr(movie, 'likes', movie.likes + 1)
        db.commit()
        db.refresh(movie)
    
    return movie


def add_dislike_to_movie(db: Session, movie_id: int):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    
    if movie:
        setattr(movie, 'dislikes', movie.dislikes + 1)
        db.commit()
        db.refresh(movie)
    
    return movie