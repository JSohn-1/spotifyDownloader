from subsonic import subsonic
from files import files
import xml.etree.ElementTree as ET
from gooey import Gooey, GooeyParser
import platform
#Create gui

@Gooey(program_name="Spotify downloader")
def main():
    parser = GooeyParser(description="Spotify to subsonic downloader.")
    parser.add_argument("-legacy_login", "-l", help="Select if the server doesn't support authentication with a salt", action="store_true")
    parser.add_argument("URL", help="URL to access the subsonic server.")
    parser.add_argument("Username", help="Username for the subsonic user.")
    parser.add_argument("Password", help="Password for the subsonic user.", widget="PasswordField")
    parser.add_argument("Playlist_link", help="Share link of the Spotify playlist. Ensure that the playlist is public.")

    parser.add_argument("Threads", help="Number of threads spotdl uses to download the playlist.")
    parser.add_argument("Location", help="Where spotdl will download the music to.", widget="DirChooser")
    
    args = parser.parse_args()

    """
    if which("spotdl") is None:
        raise Exception(f"SpotDL not installed. Please go to https://github.com/spotDL/spotify-downloader/releases/latest and download your version. ({platform.system()})")
    """
    ss = subsonic(args.Username, args.Password, args.URL, not args.legacy_login)
    s = ss.ping()
    print(ss.ping().json)
    result = ET.fromstring(s.text)
    problem = False
    response = []
    for type in result.findall("error"):
        response.append(type.get("code"))
        response.append(type.get("message"))
        problem = True
    if s.status_code != 200:
        raise Exception(s.reason)
    if problem:
        if response[0] == "10":
            if response[1] == "Required parameter 'p' is missing.":
                raise Exception(f"{response[1]} Try checking the legacy login box.")
            raise Exception(response[0])
        else:
            raise Exception(response[1])
        
    print(files.downloadPlaylist(args.Playlist_link, ss, args.Threads, args.Location))

if __name__ == '__main__':
    main()