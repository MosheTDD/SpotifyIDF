from fastapi import FastAPI
from app.routers import artists, albums, songs, auth, playlists


app = FastAPI()

app.include_router(artists.router, tags=["artists"])
app.include_router(albums.router, tags=["albums"])
app.include_router(songs.router, tags=["songs"])
app.include_router(auth.router, tags=["auth"])
app.include_router(playlists.router, tags=["playlists"])


@app.get("/")
def root():
    """
    Root endpoint of the application.

    This endpoint returns a welcome message.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Spotify app by: Moshe Khovailo"}
    