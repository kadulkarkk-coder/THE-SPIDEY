"""URL validation and navigation safety policy."""
from __future__ import annotations
from urllib.parse import urlparse

class URLPolicy:
    ALLOWED_SCHEMES = frozenset({"http", "https"})
    def validate(self, url: str) -> bool:
        parsed = urlparse(url.strip())
        return parsed.scheme.lower() in self.ALLOWED_SCHEMES and bool(parsed.netloc)
    def require_valid(self, url: str) -> str:
        value = url.strip()
        if not self.validate(value): raise ValueError("unsupported or invalid URL")
        return value
