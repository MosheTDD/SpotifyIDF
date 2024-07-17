import json
from typing import List

from app.schemas.artist import Artist

def read_artists() -> List[Artist]:
    """
    Retrieve all artists from the JSON file.

    This function reads artists data from the 'data/artists_data.json' file and converts it into a list of Artist objects.

    Returns:
        List[Artist]: A list of Artist objects.
    """
    with open('data/artists_data.json', 'r') as file:
        artists_data = json.load(file)
        return [Artist(**artist) for artist in artists_data]