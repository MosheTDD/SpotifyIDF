import json
from typing import Optional, List

from app.schemas.playlist import Playlist

def read_playlists() -> List[Playlist]:
    """
    Retrieve all playlists from the JSON file.

    This function reads playlists data from the 'data/playlists_data.json' 
    file and converts it into a list of Playlist objects.

    Returns:
        List[Playlist]: A list of Playlist objects.
    """
    with open('data/playlists_data.json', 'r') as file:
        playlists_data = json.load(file)
        return [Playlist(**playlist) for playlist in playlists_data]

def playlist_exists(name: str) -> bool:
    """
    Check if a playlist exists by name.

    This function checks if a playlist with the given name already exists.

    Args:
        name (str): The name of the playlist to check.

    Returns:
        bool: True if the playlist exists, False otherwise.
    """
    playlists = read_playlists()
    return any(playlist.title == name for playlist in playlists)

def get_playlist_by_title(title: str) -> Optional[Playlist]:
    """
    Retrieve a playlist by title.

    This function fetches a playlist with the specified title from the data source.

    Args:
        title (str): The title of the playlist.

    Returns:
        Optional[Playlist]: The playlist with the specified title, or None if not found.
    """
    playlists = read_playlists('data/playlists_data.json')
    return next((playlist for playlist in playlists if playlist.title == title), None)

def is_song_in_playlist(song_id: int, playlist: Playlist) -> bool:
    """
    Check if a song is in a playlist.

    This function checks if a song with the given ID is already in the specified playlist.

    Args:
        song_id (int): The ID of the song to check.
        playlist (Playlist): The playlist to check.

    Returns:
        bool: True if the song is in the playlist, False otherwise.
    """
    return song_id in playlist.song_ids



