# Spotify to Subsonic Migration Tool

## Easily migrate from Spotify to a subsonic server! Downloads music and either creates or updates a playlist to a subsonic API server automatically

Define users using JSON files and will go through each user, updating the corresponding playlist on the defined subsonic API server. Will also check if there have been any changes to the Spotify playlist, skipping it entirely if there were none.

Even though some servers have built-in methods to import .m3u playlists, many do not. Plus, this script will also download the music and add the metadata to the files so as to completly automate the process. All you have to do is run the script and it will do the rest! 

To use this script, create a directory in the same directory as the script called, "config" then create a .json file for each user per server. Find examples in the "Examples" directory. Links in the playlist field must be Spotify playlists.

If you want to store config files somewhere else, start the script with a directory as an argument. For example: `python3 spotifyDownloader '\etc\spot-config\'`

For `authenticate_with_hash_and_salt`, check to see if your subsonic server supports the new hash authentication. If it doesn't, set it to false

## Don't have a subsonic server? Find one on [GitHub](https://github.com/topics/subsonic-server)!

## Note: this script has certain dependencies which must be installed separately:
### TagLib
To install TagLib, click [here](https://pypi.org/project/pytaglib/) and follow the instructions for your OS before running PIP

### FFmpeg 
This script uses spotDL to download the music, which requires FFmpeg to be installed. To install FFmpeg, click [here](https://ffmpeg.org/download.html) and follow the instructions for your OS before running PIP