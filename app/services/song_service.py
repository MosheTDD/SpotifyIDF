from typing import List
from app.schemas.song import Song
from app.utils.song_utils import read_songs

def get_all_songs() -> List[Song]:
    """
    Retrieve all songs.

    This function fetches all songs from the data source using the `read_songs` utility function.

    Returns:
        List[Song]: A list of all songs.
    """
    return read_songs()

def get_top_ten_songs_by_artist_id(artist_id: int) -> List[Song]:
    """
    Retrieve the top 10 songs by artist ID.

    This function fetches the top 10 songs for a specific artist, sorted by popularity in descending order.

    Args:
        artist_id (int): The ID of the artist.

    Returns:
        List[Song]: A list of the top 10 songs for the specified artist, sorted by popularity.
    """
    songs = read_songs()
    artist_songs = [song for song in songs if artist_id in song.artist_ids]

    top_songs = sorted(artist_songs, key=lambda song: song.popularity, reverse=True)[:10]

    return top_songs

def get_songs_by_album_id(album_id: int) -> List[Song]:
    """
    Retrieve songs by album ID.

    This function fetches songs for a specific album from the data source using the `read_songs` utility function.

    Args:
        album_id (int): The ID of the album.

    Returns:
        List[Song]: A list of songs for the specified album.
    """
    songs = read_songs()
    return [song for song in songs if album_id == song.album_id]

def get_top_ten_popular_by_genre(genre: str) -> List[Song]:
    """
    Retrieve the top 10 popular songs by genre.

    This function fetches the top 10 popular songs for a specific genre, sorted by popularity in descending order.

    Args:
        genre (str): The genre of the songs.

    Returns:
        List[Song]: A list of the top 10 popular songs for the specified genre, sorted by popularity.
    """
    songs = read_songs()
    genre_songs = [song for song in songs if genre == song.genre]

    top_songs = sorted(genre_songs, key=lambda song: song.popularity, reverse=True)[:10]

    return top_songs
