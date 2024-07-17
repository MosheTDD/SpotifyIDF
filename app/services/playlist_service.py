import json
from datetime import datetime
from typing import List

from fastapi import HTTPException

from app.schemas.playlist import Playlist
from app.schemas.user import User
from app.utils.playlist_utils import read_playlists, playlist_exists, is_song_in_playlist
from app.utils.song_utils import song_exists, read_songs
from app.utils.user_utils import can_add_song_to_playlist, can_create_playlist

class PlaylistAlreadyExistsError(Exception):
    """
    Exception raised when attempting to create a playlist that already exists.

    Attributes:
        title (str): The title of the playlist that already exists.
        message (str): The error message indicating the playlist already exists.
    """
    def __init__(self, title: str):
        self.message = f"The playlist '{title}' already exists"
        super().__init__(self.message)

def create_playlist(title: str, user: User, song_id: int):
    """
    Create a new playlist.

    This function creates a new playlist with the provided title and initial song.
    It raises an exception if the user cannot create more playlists, the playlist already exists, or the song does not exist.

    Args:
        title (str): The title of the new playlist.
        user (User): The user creating the playlist.
        song_id (int): The ID of the initial song to add to the playlist.

    Returns:
        Playlist: The created playlist.

    Raises:
        HTTPException: If the user cannot create more playlists (status code 400).
        HTTPException: If the playlist already exists (status code 400).
        HTTPException: If the song does not exist (status code 404).
    """
    playlists = read_playlists()
    if not can_create_playlist(user, playlists):
        raise HTTPException(status_code=400, detail="Free users can only create up to 5 playlists")
    if playlist_exists(title):
        raise HTTPException(status_code=400, detail=f"Playlist '{title}' already exists")

    if not song_exists(song_id):
        raise HTTPException(status_code=404, detail="Song not found")

    new_playlist = Playlist(
        id=len(playlists) + 1,
        title=title,
        owner_id=user.id,
        song_ids=[song_id]
    )

    playlists.append(new_playlist)
    with open('data/playlists_data.json', 'w') as file:
        json.dump([playlist.model_dump() for playlist in playlists], file, indent=4)
    return new_playlist

def add_song_to_playlist(user: User, title: str, song_id: int) -> Playlist:
    """
    Add a song to an existing playlist.

    This function adds a song to an existing playlist. It raises an exception if the song does not exist, 
    the playlist does not exist, the user cannot add more songs to the playlist, or the song is already in the playlist.

    Args:
        user (User): The user adding the song to the playlist.
        title (str): The title of the playlist.
        song_id (int): The ID of the song to add to the playlist.

    Returns:
        Playlist: The updated playlist.

    Raises:
        HTTPException: If the song does not exist (status code 404).
        HTTPException: If the playlist does not exist (status code 404).
        HTTPException: If the user cannot add more songs to the playlist (status code 400).
        HTTPException: If the song is already in the playlist (status code 400).
    """
    if not song_exists(song_id):
        raise HTTPException(status_code=404, detail="Song not found")
    playlists = read_playlists()
    playlist = next((playlist for playlist in playlists if user.id == playlist.owner_id and title == playlist.title), None)
    
    if not can_add_song_to_playlist(user, playlist):
        raise HTTPException(status_code=400, detail="Free users can only add up to 20 songs per playlist") 

    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    if is_song_in_playlist(song_id, playlist):
        raise HTTPException(status_code=400, detail="Song already in playlist")
    
    playlist.song_ids.append(song_id)
    
    # Save the updated playlists back to the file
    with open('data/playlists_data.json', 'w') as file:
        json.dump([pl.model_dump(by_alias=True) for pl in playlists], file, indent=4, default=str)
    
    return playlist