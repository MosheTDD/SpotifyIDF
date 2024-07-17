from pydantic import BaseModel
from datetime import datetime
from typing import List

class Play(BaseModel):
    """
    Represents a play of a song with the date it was played.

    Attributes:
        play_date (datetime): The date and time when the song was played.
    """
    play_date: datetime

class Song(BaseModel):
    """
    Represents a song with a unique identifier, title, artist IDs, album ID, popularity, genre, and plays.

    Attributes:
        id (int): The unique identifier of the song.
        title (str): The title of the song.
        artist_ids (List[int]): A list of unique identifiers for the artists of the song.
        album_id (int): The unique identifier of the album the song belongs to.
        popularity (int): The popularity score of the song.
        genre (str): The genre of the song.
        plays (List[Play]): A list of plays representing when the song was played.
    """
    id: int
    title: str
    artist_ids: List[int]
    album_id: int
    popularity: int
    genre: str
    plays: List[Play] = []