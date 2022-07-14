import sys
import os
import ytmusicapi
import PyInstaller.__main__  # type: ignore
from pathlib import Path
import gooey

locales_path = str((Path(ytmusicapi.__file__).parent / "locales"))
gooey_root = os.path.dirname(gooey.__file__)

PyInstaller.__main__.run(
    [
        "src/__main__.py",
        "--icon",
        os.path.join(gooey_root, 'images', 'program_icon.ico'),
        "--onefile",
        #"--add-data",
        #f"{locales_path}{os.pathsep}ytmusicapi/locales",
        "--name",
        f"spotifyDownloader-{1}-{sys.platform}",
        "--windowed",
        "--collect-all",
        "yt_dlp",
        "--collect-all",
        "spotdl",
        "--collect-all",
        "ytmusicapi",
        "--python-option",
        " -u",
    ]
)