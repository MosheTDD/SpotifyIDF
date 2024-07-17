import json
from typing import List

from datetime import datetime, timedelta
from app.schemas.song import Play, Song
def read_songs() -> List[Song]:
    """
    Retrieve all songs from the JSON file and calculate their popularity.

    This function reads songs data from the 'data/songs_data.json' file, 
    calculates the popularity of each song based on its plays,
    and converts the data into a list of Song objects.

    Returns:
        List[Song]: A list of Song objects with calculated popularity.
    """
    with open('data/songs_data.json', 'r') as file:
        songs_data = json.load(file)
        songs = []
        for song in songs_data:
            plays = [Play(play_date=datetime.fromisoformat(play['play_date'])) for play in song['plays']]
            popularity = calculate_popularity(plays)
            songs.append(Song(
                id=song['id'],
                title=song['title'],
                album_id=song['album_id'],
                artist_ids=song['artist_ids'],
                plays=plays,
                popularity=popularity,
                genre=song['genre']
            ))
        return songs

def calculate_popularity(plays: List[Play]) -> int:
    """
    Calculate the popularity of a song based on its plays.

    This function calculates the popularity of a song by weighting its plays. 
    Plays within the last 15 days have higher weights.

    Args:
        plays (List[Play]): A list of Play objects representing when the song was played.

    Returns:
        int: The calculated popularity score of the song.
    """
    now = datetime.now()
    popularity = 0
    for play in plays:
        days_ago = (now - play.play_date).days
        weight = max(1, 15 - days_ago)
        popularity += weight
    return popularity

def song_exists(song_id: int) -> bool:
    """
    Check if a song exists by its ID.

    This function checks if a song with the given ID exists in the list of songs.

    Args:
        song_id (int): The ID of the song to check.

    Returns:
        bool: True if the song exists, False otherwise.
    """
    songs = read_songs()
    return any(song.id == song_id for song in songs)