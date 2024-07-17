from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.song import Song
from app.schemas.user import UserType
from app.services.song_service import get_all_songs, get_top_ten_popular_by_genre
from app.utils.auth_utils import get_user_from_token

router = APIRouter(
    prefix="/songs"
)

@router.get("/get-all", response_model=List[Song])
def get_all(token: str):
    """
    Retrieve all songs.

    This endpoint fetches all songs from the data source using the `get_all_songs` service function.
    If the user is a free user, only the first 5 songs are returned.

    Args:
        token (str): The JWT token of the current user.

    Returns:
        List[Song]: A list of songs, limited to 5 for free users.

    Raises:
        HTTPException: If an error occurs during the retrieval of songs, 
        an HTTP 500 error is raised with the error message.
    """
    try:
        current_user = get_user_from_token(token)
        songs = get_all_songs()
        if current_user.type == UserType.FREE:
            songs = songs[:5]
        return songs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/{genre}/top-songs", response_model=List[Song])
def get_top_songs_by_genre(genre: str, token: str):
    """
    Retrieve top 10 popular songs by genre.

    This endpoint fetches the top 10 popular songs for a specific genre from the data source using the `get_top_ten_popular_by_genre` service function.
    If the user is a free user, only the first 5 songs are returned.

    Args:
        genre (str): The genre of the songs (Pop, Rock).
        token (str): The JWT token of the current user.

    Returns:
        List[Song]: A list of the top 10 popular songs for the specified genre, limited to 5 for free users.

    Raises:
        HTTPException: If no songs are found for the specified genre, an HTTP 404 error is raised.
    """
    current_user = get_user_from_token(token)
    songs = get_top_ten_popular_by_genre(genre[0].upper() + genre[1:].lower())
    if not songs:
        raise HTTPException(status_code=404, detail="Genre Not Found")
    if current_user.type == UserType.FREE:
        songs = songs[:5]
    return songs


