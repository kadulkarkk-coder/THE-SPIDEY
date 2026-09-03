"""Normalize browser search requests without performing network access."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SearchRequest:
    query: str
    limit: int = 10

class SearchParser:
    def parse(self, query: str, limit: int = 10) -> SearchRequest:
        value = " ".join(query.split())
        if not value: raise ValueError("search query is required")
        return SearchRequest(value, max(1, min(limit, 100)))
