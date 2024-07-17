from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.artist import Artist
from app.schemas.album import Album
from app.schemas.song import Song
from app.schemas.user import UserType
from app.services.artist_service import get_all_artists
from app.services.album_service import get_albums_by_artist_id
from app.services.song_service import get_top_ten_songs_by_artist_id
from app.utils.auth_utils import get_user_from_token

router = APIRouter(
    prefix="/artists"
)

@router.get("/get-all", response_model=List[Artist])
def get_all(token: str):
    """
    Retrieve all artists.

    This endpoint fetches all artists from the data source using the `get_all_artists` service function.
    If the user is a free user, only the first 5 artists are returned.

    Args:
        token (str): The JWT token of the current user.

    Returns:
        List[Artist]: A list of artists, limited to 5 for free users.

    Raises:
        HTTPException: If an error occurs during the retrieval of artists, 
        an HTTP 500 error is raised with the error message.
    """
    try:
        current_user = get_user_from_token(token)
        artists = get_all_artists()
        if current_user.type == UserType.FREE:
            artists = artists[:5]
        return artists
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{artist_id}/albums", response_model=List[Album])
def get_albums(artist_id: int, token: str):
    """
    Retrieve albums by artist ID.

    This endpoint fetches albums for a specific artist from the data source using 
    the `get_albums_by_artist_id` service function.
    If the user is a free user, only the first 5 albums are returned.

    Args:
        artist_id (int): The ID of the artist.
        token (str): The JWT token of the current user.

    Returns:
        List[Album]: A list of albums for the specified artist, limited to 5 for free users.

    Raises:
        HTTPException: If the artist or albums are not found, 
        or if an error occurs during the retrieval, an appropriate HTTP error is raised.
    """
    current_user = get_user_from_token(token)
    albums = get_albums_by_artist_id(artist_id)
    if albums == None:
        raise HTTPException(status_code=404, detail="Artist not found")
    if not albums:
        raise HTTPException(status_code=404, detail="Albums not found")
    if current_user.type == UserType.FREE:
        albums = albums[:5]
    return albums
    
@router.get("/{artist_id}/top-songs", response_model=List[Song])
def get_top_songs(artist_id: int, token: str):
    """
    Retrieve top 10 songs by artist ID.

    This endpoint fetches the top 10 songs for a specific artist from the data source using the `get_top_ten_songs_by_artist_id` service function.
    If the user is a free user, only the first 5 songs are returned.

    Args:
        artist_id (int): The ID of the artist.
        token (str): The JWT token of the current user.

    Returns:
        List[Song]: A list of the top 10 songs for the specified artist, limited to 5 for free users.

    Raises:
        HTTPException: If no songs are found for the artist, or if an error occurs during the retrieval, an appropriate HTTP error is raised.
    """
    current_user = get_user_from_token(token)
    top_songs = get_top_ten_songs_by_artist_id(artist_id)
    if not top_songs:
        raise HTTPException(status_code=404, detail="No songs found for this artist")
    if current_user.type == UserType.FREE:
        top_songs = top_songs[:5]
    return top_songs

