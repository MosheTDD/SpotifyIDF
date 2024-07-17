from pydantic import BaseModel

class Artist(BaseModel):
    """
    Represents an artist with a unique identifier, name, and genre.

    Attributes:
        id (int): The unique identifier of the artist.
        name (str): The name of the artist.
        genre (str): The genre of music the artist is associated with.
    """
    id: int
    name: str
    genre: str