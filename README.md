# Spotify Downloader

## Easily migrate from Spotify to a subsonic server! Downloads music and creates playlist to a subsonic api server automatically


Define users using json files and will go through each user, updating the corresponding playlist on the defined subsonic api server. Will also check if there have been any changes to the spotify playlist, skipping it entirely if there was none.

To use this script, create a directory in the same directory as the script called, "config" then create a .json file for each user per server. Find examples in the "Examples" directory. Links in the playlist field must be a spotify playlist.

If you want to store config files somewhere else, start the script with a directory as an argument. For example: `python3 spotifyDownloader '\etc\spot-config\'`

For `authenticate_with_hash_and_salt`, check to see if your subsonic server supports the new hash authentication. If it doesn't, set it to false

## Don't have a subsonic server? Find one on [github](https://github.com/topics/subsonic-server)

## Note: this script has certain dependencies which must be installed sperately
### taglib
To install taglib, click [here](https://pypi.org/project/pytaglib/) and follow the instructions for your OS before running pip

### ffmpeg
This script uses spotDL to download the music, which requires ffmpeg to be installed. To install ffmpeg, click [here](https://ffmpeg.org/download.html) and follow the instructions for your OS before running pip