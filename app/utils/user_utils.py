from app.schemas.user import User, UserType
from app.schemas.playlist import Playlist
from typing import List

def can_create_playlist(user: User, playlists: List[Playlist]) -> bool:
    """
    Check if a user can create a new playlist.

    This function checks if a user can create a new playlist based on their user type.
    Free users can only create up to 5 playlists.

    Args:
        user (User): The user attempting to create a playlist.
        playlists (List[Playlist]): The list of playlists already created by the user.

    Returns:
        bool: True if the user can create a new playlist, False otherwise.
    """
    if user.type == UserType.FREE and len(playlists) >= 5:
        return False
    return True

def can_add_song_to_playlist(user: User, playlist: Playlist) -> bool:
    """
    Check if a user can add a song to a playlist.

    This function checks if a user can add a song to a playlist based on their user type.
    Free users can only add up to 20 songs per playlist.

    Args:
        user (User): The user attempting to add a song to the playlist.
        playlist (Playlist): The playlist to which the user is attempting to add a song.

    Returns:
        bool: True if the user can add a song to the playlist, False otherwise.
    """
    if user.type == UserType.FREE and len(playlist.song_ids) >= 20:
        return False
    return True