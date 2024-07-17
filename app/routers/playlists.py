from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.schemas.playlist import Playlist
from app.schemas.user import User
from app.services.playlist_service import create_playlist, add_song_to_playlist, PlaylistAlreadyExistsError
from app.utils.auth_utils import get_user_from_token

router = APIRouter(
    prefix="/playlists"
)

@router.post("/create-new-playlist", response_model=Playlist)
def create_new_playlist(title: str, song_id: int, token: str):
    """
    Create a new playlist.

    This endpoint creates a new playlist with the provided title and initial song.
    The current user is determined from the provided token.
    
    Args:
        title (str): The title of the new playlist.
        song_id (int): The ID of the initial song to add to the playlist.
        token (str): The JWT token of the current user.

    Returns:
        Playlist: The created playlist.

    Raises:
        HTTPException: If a playlist with the same title already exists (status code 409),
                       or if any other error occurs (status code 500).
    """
    try:
        current_user = get_user_from_token(token)
        playlist = create_playlist(title, current_user, song_id)
        return playlist
    except PlaylistAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/playlists/{title}/add-song", response_model=Playlist)
def add_song(title: str, song_id: int, token: str):
    """
    Add a song to an existing playlist.

    This endpoint adds a song to an existing playlist.
    The current user is determined from the provided token.
    
    Args:
        title (str): The title of the playlist.
        song_id (int): The ID of the song to add to the playlist.
        token (str): The JWT token of the current user.

    Returns:
        Playlist: The updated playlist.

    Raises:
        HTTPException: If any error occurs during the process (status code 500).
    """
    try:
        current_user = get_user_from_token(token)
        playlist = add_song_to_playlist(current_user, title, song_id)
        return playlist
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
        