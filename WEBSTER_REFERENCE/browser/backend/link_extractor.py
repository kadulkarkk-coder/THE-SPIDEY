"""Extract and normalize links from HTML."""
from __future__ import annotations
from html import unescape
from urllib.parse import urljoin
import re

class LinkExtractor:
    _pattern = re.compile(r'''<a\\b[^>]*?href=["']([^"']+)["']''', re.I)
    def extract(self, html: str, base_url: str | None = None) -> tuple[str, ...]:
        links = []
        for raw in self._pattern.findall(html or ""):
            value = unescape(raw.strip())
            if base_url: value = urljoin(base_url, value)
            if value and value not in links: links.append(value)
        return tuple(links)
