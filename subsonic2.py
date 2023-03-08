import time
import libsonic
import os
import taglib
from time import sleep
class subsonic(libsonic.Connection):
    # Seperate the port from the url and pass it to the libsonic connection and if there is none then make the port 80 if http and 443 if https
    def __init__(self, url, username, password, legacy=False):

        if "http" not in url:
            raise Exception("Invalid URL; must start with http or https")
        port = None
        # If the url has https in it then make the port 443
        if "https" in url:
            port = 443

        # pop the port at the end of the url and set port to it if present and remove the port from the url. do not remove http
        if ":" in url.split("://")[1].split("/")[0]:
            port = url.split("://")[1].split("/")[0].split(":")[1]
            url = url.split("://")[0] + "://" + url.split("://")[1].split("/")[0].split(":")[0] + "/" + "/".join(url.split("://")[1].split("/")[1:])

        # If the port is still None then make the port 80
        if port is None:
            port = 80

        # Remove the slash at the end of url if present
        if url[-1] == "/":
            url = url[:-1]

        # Pass the url, username, password, legacyAuth, and port to the libsonic connection
        super().__init__(url, username, password, legacyAuth=legacy, port=port)


    # Wrapper for the getScanStatus to return a boolean instead of a dict
    def getScanStatus(self):
        return super().getScanStatus()['scanStatus']['scanning']

    # Wrapper for the libsonic getUser function to have a default username of the current user
    def getUser(self, username=None):  
        if username is None:
            username = self.username
        return super().getUser(username)

    def isAdmin(self, username=None):
        if username is None:
            username = self.username
        return self.getUser(username)['user']['adminRole']

    def findSongId(self, song_name):
        offset = 0
        while True:
            
            results = self.search2(song_name, artistCount=0, albumCount=0, songOffset=offset)['searchResult2']
            # Check if results is empty and if so then break
            if results == {}:
                break
            
            results = results['song']
            for song in results:
                if song['title'] == song_name:
                    return song['id']

            offset += 20
            if len(results) < 20:
                break
        raise Exception(f"Song '{song_name}' not found")
    
    def findAlbumId(self, album_name):
        offset = 0
        while True:
            results = self.search2(album_name, artistCount=0, songCount=0, albumOffset=offset)['searchResult2']['album']
            
            for album in results:
                if album['name'] == album_name:
                    return album['id']

            offset += 20
            if len(results) < 20:
                break
        raise Exception(f"Album '{album_name}' not found")
    
    def findPlaylistId(self, playlist_name, username=None, own=True):
        playlists = self.getPlaylists(username=username)['playlists']

        # Make sure playlist exists
        if 'playlist' not in playlists:
            raise Exception("Playlist not found")

        playlists = playlists['playlist']
        if isinstance(playlists, dict):
            playlists = [playlists]

        for playlist in playlists:
            if playlist['name'] == playlist_name:
                if (own and playlist["owner"] == self.username) or not own:
                    return playlist['id']

        raise Exception("Playlist not found")
    
    def playlistExists(self, playlist_name, username=None):
        playlists = self.getPlaylists(username=username)['playlists']

        # Make sure playlist exists
        if 'playlist' not in playlists:
            return False

        playlists = playlists['playlist']
        if isinstance(playlists, dict):
            playlists = [playlists]

        for playlist in playlists:
            if playlist['name'] == playlist_name and playlist["owner"] == username:
                return True
        return False
    
    def isSongInPlaylist(self, playlist_id, song_id, index=None):
        playlist = self.getPlaylist(playlist_id)
        for song in playlist:
            if song['id'] == song_id:
                if index is not None:
                    if song['index'] == index:
                        return True
                else:
                    return True
        return False
    def createPlaylistFromM3U(self, m3u_file, replace=True, playlist_name=None, own=True, increment=100):
        """
        Reads a M3U file and creates a playlist on the server using the taglib
        package to find the title of the song files. If `playlist_name` is not
        provided, the name of the playlist will be the name of the M3U file. If
        `replace` is True and a playlist with the same name already exists, it
        will be replaced with the new playlist. If `replace` is False and a
        playlist with the same name already exists, a new playlist with a unique
        name will be created.
        """
        if playlist_name is None:
            playlist_name = os.path.basename(m3u_file)

        # Check if a playlist with the same name already exists

        if own:
            username = self.username
        else:
            username = None

        if replace and self.playlistExists(playlist_name, username):
            # Fixed bug where the playlist wouldn't be deleted fast enough
            while self.playlistExists(playlist_name, username):
                self.deletePlaylist(self.findPlaylistId(playlist_name, username))
        elif not replace and self.playlistExists(playlist_name, username):
            playlist_names = self.getPlaylists(username)
            i = 1
            while True:
                new_name = f"{playlist_name} ({i})"
                if new_name not in playlist_names:
                    playlist_name = new_name
                    break
                i += 1

        # Create the new playlist on the server
        self.createPlaylist(name=playlist_name)
        playlist_id = self.findPlaylistId(playlist_name, username, own)
        songs = []
        # Read the M3U file and add the songs to the playlist
        with open(m3u_file, "r", encoding='utf-8') as f:
            totalSongs = 0
            totalInFile = 0
            for line in f:
                totalInFile += 1
                # Open the song file and retrieve the title tag
                try:
                    song_file = taglib.File(line.strip())
                except:
                    print(line.strip())
                    continue
                
                # Once title is recorded, closes the song to reduce memory usage and allow other programs to access the files
                title = song_file.tags["TITLE"][0]                    
                song_file.close()
                try:
                    id = self.findSongId(title)
                except:
                    raise Exception(song_file)
                """
                # Keeps looping until the playlist is actually updated. Weird problem where the update wouldn't actually happen for some reason
                while not self.is_song_in_playlist(playlist_id, id, index=totalSongs):
                    self.addToPlaylist(playlist_id, id)
                """
                songs.append(id)
                totalSongs += 1

        # Add the songs to the playlist at a certain amount at a time as defined by the increment variable
        for i in range(0, len(songs), increment):
            self.updatePlaylist(playlist_id, songIdsToAdd=songs[i:i+increment])
        
        print(f"Total songs in file: {totalInFile}")
        print(f"Total songs: {totalSongs}")
        return playlist_id
