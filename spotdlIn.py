from spotdl import Spotdl
from spotdl.utils.config import DEFAULT_CONFIG
class spotdlin:
    def __init__(format, threads, url):
        self.spotdl = Spotdl(client_id=DEFAULT_CONFIG["client_id"], client_secret=DEFAULT_CONFIG["client_secret"])
        self.format = format
        self.threads = threads
        self.url = url