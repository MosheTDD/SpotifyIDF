from typing import List

from app.schemas.album import Album
from app.utils.album_utils import read_albums


def get_all_albums() -> List[Album]:
    """
    Retrieve all albums.

    This function fetches all albums from the data source using the `read_albums` utility function.

    Returns:
        List[Album]: A list of all albums.
    """
    return read_albums()

def get_albums_by_artist_id(artist_id: int) -> List[Album]:
    """
    Retrieve albums by artist ID.

    This function fetches albums for a specific artist from the data source using the `read_albums` utility function.

    Args:
        artist_id (int): The ID of the artist.

    Returns:
        List[Album]: A list of albums associated with the specified artist ID.
    """
    albums = read_albums()
    return [album for album in albums if artist_id in album.artist_ids]

