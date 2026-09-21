"""Natural-language file-search intent extraction for WEBSTER A14."""
from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class FileSearchIntent:
    is_search: bool
    query: str = ""
    limit: int = 5


class FileSearchIntentParser:
    _PATTERNS = (
        r"^\s*(?:search|find|look\s+for|locate)\s+(?:a\s+)?file(?:s)?\s+(?:about|containing|that\s+(?:mentions?|contains?)|with|related\s+to)\s+(.+?)\s*$",
        r"^\s*(?:search|find|look\s+for|locate)\s+(?:through\s+)?(?:my\s+)?files?\s+(?:for|about|containing|related\s+to)\s+(.+?)\s*$",
        r"^\s*can\s+you\s+(?:search|find|locate)\s+(?:a\s+)?file(?:s)?\s+(?:about|containing|related\s+to)\s+(.+?)\s*$",
        r"^\s*find\s+the\s+(?:document|file)\s+(?:where|that)\s+(.+?)\s*$",
    )

    def parse(self, text: str) -> FileSearchIntent:
        cleaned = " ".join(text.strip().split())
        for pattern in self._PATTERNS:
            match = re.match(pattern, cleaned, re.I)
            if match:
                query = match.group(1).strip(" .?!")
                if len(query) >= 3:
                    return FileSearchIntent(True, query)

        if re.search(r"\b(?:file|files|document|documents)\b", cleaned, re.I) and re.search(
            r"\b(?:search|find|locate|look)\b", cleaned, re.I
        ):
            query = re.sub(
                r"\b(?:search|find|locate|look|for|a|the|my|file|files|document|documents)\b",
                " ",
                cleaned,
                flags=re.I,
            )
            query = " ".join(query.split()).strip(" .?!")
            if len(query) >= 3:
                return FileSearchIntent(True, query)

        return FileSearchIntent(False)
