"""Safe page-content normalization and extraction boundary."""
from __future__ import annotations
from html import unescape
import re

class PageReader:
    def text(self, html: str, *, max_chars: int = 20000) -> str:
        if max_chars < 1: raise ValueError("max_chars must be positive")
        cleaned = re.sub(r"<(script|style)\\b[^>]*>.*?</\\1>", " ", html or "", flags=re.I | re.S)
        cleaned = re.sub(r"<[^>]+>", " ", cleaned)
        cleaned = unescape(cleaned)
        return " ".join(cleaned.split())[:max_chars]
    def title(self, html: str) -> str | None:
        match = re.search(r"<title[^>]*>(.*?)</title>", html or "", flags=re.I | re.S)
        return " ".join(unescape(match.group(1)).split()) if match else None
