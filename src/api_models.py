from enum import Enum
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