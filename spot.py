import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

client_id, client_secret = "5f573c9620494bae87890c0f08a60293", "212476d9b0f3472eaa762d90b19b0ba8"
# Set up client credentials manager
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Get the name of a spotify playlist from a url using spotipy
@staticmethod
def playlistName(url):
    return sp.playlist(getId(url))['name']

# Get the contents of a spotify playlist from a url using spotipy in the same form as spotdl: artists seperated by commas - song title
@staticmethod
def playlistContents(url):
    # Get all of the tracks of the playlist, accounting for the fact that the playlist may be split into multiple pages
    playlist_id = getId(url)
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # Get the artist and song name for each track
    contents = []
    for track in tracks:
        artists = []
        for artist in track['track']['artists']:
            artists.append(artist['name'])
        contents.append(f"{' & '.join(artists)} - {track['track']['name']}")

    return contents




@staticmethod
def getId(url):
    return re.search(r"playlist/(\w+)", url).group(1)