from time import sleep
from subsonic import subsonic
import os
import subprocess
from pathlib import Path
#from win32com.client import Dispatch
from shutil import which
from sys import platform
import taglib

from spotdl.search import SpotifyClient
from spotdl.parsers import parse_query
from spotdl.download import DownloadManager
from spotdl.download import ffmpeg, DownloadManager

class files:
    @staticmethod
    def downloadPlaylist(url, ss, threads, directory, format):
        SpotifyClient.init(
            client_id="5f573c9620494bae87890c0f08a60293",
            client_secret="212476d9b0f3472eaa762d90b19b0ba8",
            user_auth=False
        )
        spotdl_opts = {
            "query": [url],
            "output_format": format,
            "download_threads": int(threads),
            "use_youtube": False,
            "generate_m3u": True,
            "search_threads": int(threads),
            "lyrics-provider": "musixmatch",            
            "path_template": None,
            "threads": int(threads)

        }
        
        os.chdir(directory)
        
        with DownloadManager(spotdl_opts) as downloader:
            # Get songs
            song_list = parse_query(                
                spotdl_opts["query"],                
                spotdl_opts["output_format"],                
                spotdl_opts["use_youtube"],
                spotdl_opts["generate_m3u"],
                spotdl_opts["lyrics-provider"],
                spotdl_opts["threads"],
                spotdl_opts["path_template"],
            )

            # Start downloading
            if len(song_list) > 0:
                downloader.download_multiple_songs(song_list)
        
        
        """
        if which("spotdl") is None or which("spotdl.exe") is None:
            print("Spotdl not found! Installing...")
            if platform == "linux" or platform == "linux2":
                print("Linux detected")
                subprocess.call("pip3 install Spotdl")
                py = True
            else:
                response = requests.get("https://api.github.com/repos/spotDL/spotify-downloader/releases/latest")
                downloads = {}
                for i in response.json()["assets"]:
                    if "darwin" in i["name"]:
                        downloads["darwin"] = i["browser_download_url"]
                        downloads["name"] = i["name"]

                    elif "win32" in i ["name"]:
                        downloads["win32"] = i["browser_download_url"]
                        downloads["name"] = i["name"]

                if platform == "darwin":
                    print("MacOS detected")
                    subprocess.call("curl -Lo spotdl " + downloads["darwin"])

                elif platform == "win32":
                    print("Windows detected")
                    subprocess.call("curl -Lo spotdl.exe " + downloads["win32"])

        #Start download
        if platform == "linux" or platform == "linux2":
            files.process(f"python3 -m spotdl download {url} --format {format} --threads {threads} --generate-m3u")
        elif platform == "darwin":
            files.process(f"spotdl download {url} --format {format} --threads {threads} --generate-m3u")
        else:
            files.process(f"spotdl.exe download {url} --format {format} --threads {threads} --generate-m3u")
        """

        #Wait until scan finished
        ss.scan()
        while(ss.getScanStatus()):
            sleep(0.01)

        #Read playlist file
        x = ""
        y = ""
        for file in os.listdir():
            if file.endswith(".m3u"):
                x = file
                y = file
        f = open(x, "r", encoding="utf-8")
        n = f.read().splitlines()
       # print(n)
        titles = []
        #Read files for title
        for i in n:
            titles.append(files.getTitle(i))
        print("Amount of songs: " + str(len(titles)))
        n = []
        for i in titles:
            n.append(ss.getId(i))

        #name = []
        print("Number of songs: " + str(len(n)))

        
        ss.createPlaylist(os.path.splitext(x)[0])
        print(len(n))
        ss.addToPlaylist(ss.getPId(os.path.splitext(x)[0]), n)
        f.close()
        os.remove(y)
        return(n)

    @staticmethod
    def parseName(name):
        o = name
        name = list(name)
        x = []

        for i in range(o.find("-") + 2, len(o)):
            x.append(name[i])

        """
        for i in range(len(name) - 1, -1, -1):
            if name[i] == "-":
                for n in range(i + 2, len(name)):
                    x.append(name[n])
                #print("done")
                break
                
        print("".join(x))
        name = []
        for i in range(len(x) - 1, 0, -1):
            print(x[i])
            if x[i] == ".":
                for n in range(i):
                    name.append(x[n])
                    #print(name)
        #print("".join(name))

        """

        name =  "".join(x)

        
        return Path(name).stem
    """
    @staticmethod
    def getTitle(file):
        return files.getFileProperties(file)["Title"]

    @staticmethod
    def getFileProperties(fname):
        shell = Dispatch("Shell.Application")
        _dict = {}
        # enter directory where your file is located
        ns = shell.NameSpace(os. getcwd())
        for i in ns.Items():
            # Check here with the specific filename
            if str(i) == fname:
                for j in range(0,49):
                    _dict[ns.GetDetailsOf(j,j)] = ns.GetDetailsOf(i,j)

        return(_dict)
    """
    @staticmethod
    def getTitle(file):
        return taglib.File(file).tags["TITLE"][0]

    @staticmethod
    def process(p):
        process = subprocess.Popen(p, 
        bufsize=1, 
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        shell=True
        )

        for line in process.stdout:
            print(line)