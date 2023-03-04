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
    playlist_id = re.search(r"playlist/(\w+)", url).group(1)
    return sp.playlist(playlist_id)

# Get the contents of a spotify playlist from a url using spotipy in the same form as spotdl: artiists seperated by commas - song title
@staticmethod
def playlistContents(url):
    playlist_id = re.search(r"playlist/(\w+)", url).group(1)
    playlist = sp.playlist(playlist_id)
    playlist_tracks = playlist['tracks']['items']
    playlist_contents = []
    for track in playlist_tracks:
        artists = []
        for artist in track['track']['artists']:
            artists.append(artist['name'])
        artists = ", ".join(artists)
        title = track['track']['name']
        playlist_contents.append(f"{artists} - {title}")
    return playlist_contents

@staticmethod
def getId(url):
    return re.search(r"playlist/(\w+)", url).group(1)