from pydantic import BaseModel
from typing import List

class Album(BaseModel):
    """
    Represents an album with a unique identifier, title, and a list of artist IDs.

    Attributes:
        id (int): The unique identifier of the album.
        title (str): The title of the album.
        artist_ids (List[int]): A list of artist IDs associated with the album.
    """
    id: int
    title: str
    artist_ids: List[int]