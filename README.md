# Spotify Downloader

## Downloads music and creates playlist to a subsonic api server

Define users using json files and will go through each user, updating the corresponding playlist on the defined subsonic api server. Will also check if there have been any changes to the spotify playlist, skipping it entirely if there was none.

To use this script, create a directory in the same directory as the script called, "config" then create a .json file for each user per server. Find examples in the "Examples" directory. Links in the playlist field must be a spotify playlist.

If you want to store config files somewhere else, start the script with a directory as an argument. For example: `python3 spotifyDownloader '\etc\spot-config\'`

For `authenticate_with_hash_and_salt`, check to see if your subsonic server supports the new hash authentication. If it doesn't, set it to false
