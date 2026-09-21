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
        r"^s*(?:search|find|looks+for|locate)s+(?:as+)?file(?:s)?s+(?:about|containing|thats+(?:mentions?|contains?)|with|relateds+to)s+(.+?)s*$",
        r"^s*(?:search|find|looks+for|locate)s+(?:throughs+)?(?:mys+)?files?s+(?:for|about|containing|relateds+to)s+(.+?)s*$",
        r"^s*cans+yous+(?:search|find|locate)s+(?:as+)?file(?:s)?s+(?:about|containing|relateds+to)s+(.+?)s*$",
        r"^s*finds+thes+(?:document|file)s+(?:where|that)s+(.+?)s*$",
    )

    def parse(self, text: str) -> FileSearchIntent:
        cleaned = " ".join(text.strip().split())
        for pattern in self._PATTERNS:
            match = re.match(pattern, cleaned, re.I)
            if match:
                query = match.group(1).strip(" .?!")
                if len(query) >= 3:
                    return FileSearchIntent(True, query)
        # Natural phrasing without a filename: content is the query.
        if re.search(r"(?:file|files|document|documents)", cleaned, re.I) and re.search(
            r"(?:search|find|locate|look)", cleaned, re.I
        ):
            query = re.sub(r"(?:search|find|locate|look|for|a|the|my|file|files|document|documents)", " ", cleaned, flags=re.I)
            query = " ".join(query.split()).strip(" .?!")
            if len(query) >= 3:
                return FileSearchIntent(True, query)
        return FileSearchIntent(False)
