"""B14 browser navigation."""
from urllib.parse import quote_plus
from .system_interface import SystemInterface
class BrowserControl:
    def __init__(self): self.system=SystemInterface()
    def open(self,url): return self.system.open_url(url)
    def search(self,q): return self.open("https://www.google.com/search?q="+quote_plus(q[:300]))