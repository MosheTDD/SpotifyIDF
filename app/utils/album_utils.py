import json
from typing import List

from app.schemas.album import Album

def read_albums() -> List[Album]:
    """
    Retrieve all albums from the JSON file.

    This function reads albums data from the 'data/albums_data.json' file and converts it into a list of Album objects.

    Returns:
        List[Album]: A list of Album objects.
    """
    with open('data/albums_data.json', 'r') as file:
        albums_data = json.load(file)
        return [Album(**album) for album in albums_data]