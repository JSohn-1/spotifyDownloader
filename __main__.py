try:
    import json
    import os
    from subsonic2 import subsonic as SubsonicClient
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import subprocess
    from time import sleep
    from spot import *
    import sys
except ImportError as e:
    print(f"Error: {e}")
    print("Please install the required packages listed in requirements.txt using pip.")
    sys.exit()

# Client creds
client_id, client_secret = "5f573c9620494bae87890c0f08a60293", "212476d9b0f3472eaa762d90b19b0ba8"

# Set up client credentials manager
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Configuration:
  def __init__(self, config_file):
    self.config_file = config_file
    self.config = self._load_config()

  def _load_config(self):
    with open(self.config_file, 'r') as f:
      return json.load(f)

  def save_config(self):
    with open(self.config_file, 'w') as f:
      json.dump(self.config, f, indent=2)

  @property
  def server(self):
    return self.config['server']

  @property
  def playlists(self):
    return self.config['playlists']

downloading_playlists = []

def download_playlist(server, url, threads, dir=None, format="mp3", lyrics="genius", bitrate=320, explicit=False, update=True, admin=None):
    # Get the name of the playlist from the url
    playlist_name = playlistName(url)

    print(f"----------------------------------------- Playlist {playlist_name} starting -----------------------------------------")

    spotdl_opts = {
        "format": format,
        "threads": int(threads),
        "use_youtube": False,
        "lyrics": lyrics,            
        "path_template": None,
        "threads": int(threads),
        "bitrate": bitrate
    }
    # Download Music
    curDir = os.getcwd()
    if dir is not None:
        os.chdir(dir)

    command = ["spotdl"]
    command.append(url)
    for key, value in spotdl_opts.items():
        if value is not None:
            if isinstance(value, bool):
                if value:
                    command.append(f"--{key}")
            elif isinstance(value, list):
                for item in value:
                    command.append(f"--{key}")
                    command.append(item)
            else:
                command.append(f"--{key}")
                command.append(str(value))

    command.append("--m3u")
    # Download the track using spotdl
    subprocess.run(command)
    
    if server.isAdmin(server.username):
        server.startScan()
        while server.getScanStatus():
            sleep(0.01)
    else:
        admin.startScan()
        while admin.getScanStatus():
            sleep(0.01)

    #Create Playlist
    server.createPlaylistFromM3U(playlist_name + ".m3u8.m3u8", replace=update, playlist_name=playlist_name)

    # Delete .m3u file if it exists
    if os.path.exists(playlist_name + ".m3u8.m3u8"):
        os.remove(playlist_name + ".m3u8.m3u8")
    else:
        raise Exception("eeeeeeeeeeeeeeee")
    
    os.chdir(curDir)
    print(f"----------------------------------------- Playlist {playlist_name} downloaded -----------------------------------------")
    return([server, playlist_name + ".m3u"])

def download_playlists(client: SubsonicClient, config: Configuration, admin: SubsonicClient, config_location, check):
    print(f"Downloading for user: " + client.username)
    # Read the .cache file in the config_location directory which is a json file using the Configuration class. The key is the spotify url and the value is a list of songs in the playlist
    # Get the playlist from the subsonic server, and if they completly match, then skip the playlist
    # If they don't match, then download the playlist and update the .cache file

    #Check if the .cache file exists
    if os.path.exists(os.path.join(config_location, ".cache")):
        #Dont use the Configuration class because it doesn't work with the .cache file
        with open(os.path.join(config_location, ".cache"), 'r') as f:
            cache = json.load(f)
    else:
        cache = {}
        
    for playlist in config.playlists:
        playlist_id = getId(playlist['url'])

        if playlist_id in cache:
            # Check if the playlist has changed
            playlist_tracks = playlistContents(playlist['url'])
            playlist_name = playlistName(playlist["url"])
            if playlist_tracks == cache[playlist_id] and client.playlistExists(playlist_name, client.username) and (playlist_id not in downloading_playlists):
                print(f"Playlist {playlist_name} has not changed, skipping...")
                
            else:
                print(f"Playlist {playlist_name} has changed, downloading...")
                # Download the playlist
                download_playlist(client, playlist["url"], config.server["threads"], dir=config.server["dir"], format=config.server["format"], lyrics=config.server["lyrics"], bitrate=config.server["bitrate"], update=config.server["update"], admin=admin)
                # Update the cache
                cache[playlist_id] = playlist_tracks
                downloading_playlists.append(playlist_id)
                
        else:
            playlist_name = playlistName(playlist["url"])
            print(f"Playlist {playlist_name} has not been downloaded before, downloading...")
            # Download the playlist
            download_playlist(client, playlist["url"], config.server["threads"], dir=config.server["dir"], format=config.server["format"], lyrics=config.server["lyrics"], bitrate=config.server["bitrate"], update=config.server["update"], admin=admin)
            # Update the cache
            cache[playlist_id] = playlistContents(playlist['url'])
            downloading_playlists.append(playlist_id)


    # Save the cache
    with open(os.path.join(config_location, ".cache"), 'w') as f:
        json.dump(cache, f, indent=2)

def download_all_playlists(path_to_configs: str, check=False):
    config_files = [f for f in os.listdir(path_to_configs) if f.endswith('.json')]

    # Make sure that all links for the playlist directory is valid
    for config_file in config_files:
        config = Configuration(os.path.join(path_to_configs, config_file))
        server_config = config.server
        base_url = server_config['url']
        username = server_config['user']
        password = server_config['pass']
        use_salt = not server_config["authenticate_with_hash_and_salt"]
        client = SubsonicClient(base_url, username, password, use_salt)
        for playlist in config.playlists:
            if not isPlaylist(playlist['url']):
                raise Exception(f"Invalid url: {playlist['url']}")

    # Find an admin account for each subsonic server
    admin = {}

    for config_file in config_files:
        config = Configuration(os.path.join(path_to_configs, config_file))
        server_config = config.server
        base_url = server_config['url']
        username = server_config['user']
        password = server_config['pass']
        use_salt = not server_config["authenticate_with_hash_and_salt"]
        client = SubsonicClient(base_url, username, password, use_salt)

        if client.isAdmin(client.username):
            admin[f'{client.baseUrl}:{client.port}'] = client
    
    # Ensure there is an admin account for every subsonic server
    fail = []
    for config_file in config_files:
        config = Configuration(os.path.join(path_to_configs, config_file))
        server_config = config.server
        
        if server_config['url'] not in admin and server_config['url'] not in fail:
            fail.append(server_config['url'])

    if fail:
        raise Exception(f'Admin not found for servers: {", ".join(fail)}')

    for config_file in config_files:
        config = Configuration(os.path.join(path_to_configs, config_file))
        server_config = config.server
        base_url = server_config['url']
        username = server_config['user']
        password = server_config['pass']
        use_salt = not server_config["authenticate_with_hash_and_salt"]
        client = SubsonicClient(base_url, username, password, use_salt)

        download_playlists(client, config, admin[base_url], path_to_configs, check)

    print("----------------------------------------- Files Downloaded -----------------------------------------")
    print("Saving playlists...")

def main():
    # Get the config directory from a command line argument and if none is specficied use the default, which is './config' in the current directory
    config_location = sys.argv[1] if len(sys.argv) > 1 else "./config"

    # Check if the config directory exists and has at least one config file and if not create config directory and raise error
    if not os.path.exists(config_location):
        os.mkdir(config_location) 
        raise Exception("No config files found. Please create a config file in the config directory and try again.")

    # Check to make sure there are files in the config directory
    if not os.listdir(config_location):
        raise Exception("No config files found. Please create a config file in the config directory and try again.")

    # Check to make sure spotdl is installed
    try:
        import spotdl
    except ImportError:
        raise Exception("Spotdl is not installed. Please install spotdl and try again.")

    download_all_playlists(config_location)
    print("done")

if __name__ == '__main__':
    main()