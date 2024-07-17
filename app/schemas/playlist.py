from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.schemas.song import Song

class Playlist(BaseModel):
    """
    Represents a playlist with a unique identifier, title, owner ID, and a list of song IDs.

    Attributes:
        id (int): The unique identifier of the playlist.
        title (str): The title of the playlist.
        owner_id (int): The unique identifier of the owner of the playlist.
        song_ids (List[int]): A list of unique identifiers of the songs in the playlist.
    """
    id: int
    title: str
    owner_id: int
    song_ids: List[int]