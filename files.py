from time import sleep
from subsonic import subsonic
import os
import subprocess
from pathlib import Path
#from win32com.client import Dispatch
from shutil import which
from sys import platform
import taglib
import requests

class files:
    @staticmethod
    def downloadPlaylist(url, ss, threads, directory):
        os.chdir(directory)
        py = False
        #Check if spotdl is installed
        if which("spotdl") is None:
            if platform == "linux" or platform == "linux2":
                os.system("pip3 install Spotdl")
                py = True
            if not py:
                response = requests.get("https://api.github.com/repos/spotDL/spotify-downloader/releases/latest")
                downloads = {}
                for i in response.json()["assets"]:
                    if "darwin" in i["name"]:
                        downloads["darwin"] = i["browser_download_url"]
                    elif "win32" in i ["name"]:
                        downloads["win32"] = i["browser_download_url"]
                if platform == "darwin":
                    os.system("curl " + downloads["darwin"])
                elif platform == "win32":
                    os.system("curl " + downloads["win32"])
                

        #Start download
        #process = subprocess.run(f"spotdl --output-format flac --download-threads {threads} {url} --generate-m3u", shell=True)

        
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