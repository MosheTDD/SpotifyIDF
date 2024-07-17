from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.album import Album
from app.schemas.song import Song
from app.schemas.user import UserType
from app.services.album_service import get_all_albums
from app.services.song_service import get_songs_by_album_id
from app.utils.auth_utils import get_user_from_token

router = APIRouter(
    prefix="/albums"
)

@router.get("/get-all", response_model=List[Album])
def get_all(token: str):
    """
    Retrieve all albums.

    This endpoint fetches all albums from the data source using the `get_all_albums` service function.
    If the user is a free user, only the first 5 albums are returned.

    Args:
        token (str): The JWT token of the current user.

    Returns:
        List[Album]: A list of albums, limited to 5 for free users.

    Raises:
        HTTPException: If an error occurs during the retrieval of albums, 
        an HTTP 500 error is raised with the error message.
    """
    try:
        current_user = get_user_from_token(token)
        albums = get_all_albums()
        if current_user.type == UserType.FREE:
            albums = albums[:5]
        return albums
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{album_id}/all-songs", response_model=List[Song])
def get_album_songs(album_id: int, token: str):
    """
    Retrieve songs by album ID.

    This endpoint fetches songs for a specific album from the data source using 
    the `get_songs_by_album_id` service function.
    If the user is a free user, only the first 5 songs are returned.

    Args:
        album_id (int): The ID of the album.
        token (str): The JWT token of the current user.

    Returns:
        List[Song]: A list of songs for the specified album, limited to 5 for free users.

    Raises:
        HTTPException: If no songs are found for the specified album, an HTTP 404 error is raised.
    """
    current_user = get_user_from_token(token)
    songs = get_songs_by_album_id(album_id)
    if not songs:
        raise HTTPException(status_code=404, detail="Album Not Found")
    if current_user.type == UserType.FREE:
            songs = songs[:5]
    return songs

