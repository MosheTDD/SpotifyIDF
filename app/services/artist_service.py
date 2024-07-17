from typing import List
from app.schemas.artist import Artist
from app.utils.artist_utils import read_artists

def get_all_artists() -> List[Artist]:
    """
    Retrieve all artists.

    This function fetches all artists from the data source using the `read_artists` utility function.

    Returns:
        List[Artist]: A list of all artists.
    """
    return read_artists()