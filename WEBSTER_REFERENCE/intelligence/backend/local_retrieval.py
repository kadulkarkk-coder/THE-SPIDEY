"""Local semantic-style retrieval for WEBSTER.

Uses deterministic token normalization, lightweight concept expansion and content
evidence. No external model or service is required.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from .content_file_index import ContentFileIndex, FileSearchResult


CONCEPT_GROUPS = (
    {"photosynthesis", "plant", "plants", "chlorophyll", "light", "glucose", "food"},
    {"python", "programming", "code", "coding", "script", "software"},
    {"science", "experiment", "laboratory", "lab", "hypothesis"},
    {"math", "mathematics", "calculation", "equation", "number"},
    {"history", "historical", "war", "empire", "kingdom", "civilization"},
    {"geography", "climate", "river", "mountain", "soil", "environment"},
    {"school", "class", "chapter", "lesson", "homework", "study", "exam"},
    {"calendar", "schedule", "event", "meeting", "appointment"},
    {"task", "project", "work", "plan", "goal"},
)


@dataclass(frozen=True)
class RetrievalHit:
    path: str
    score: float
    excerpt: str
    matched_terms: tuple[str, ...]
    reason: str


class LocalRetriever:
    """Turns a local content index into bounded evidence for reasoning."""

    def __init__(self, index: ContentFileIndex) -> None:
        self.index = index

    @staticmethod
    def expand_query(query: str) -> set[str]:
        terms = set(re.findall(r"[a-zA-Z0-9_]{3,}", query.lower()))
        expanded = set(terms)
        for group in CONCEPT_GROUPS:
            if terms & group:
                expanded.update(group)
        return expanded

    def retrieve(self, query: str, *, limit: int = 5) -> tuple[RetrievalHit, ...]:
        expanded = self.expand_query(query)
        if not expanded:
            return ()
        # Existing index remains the source of truth; score its content evidence
        # again with deterministic concept expansion.
        candidates = self.index.search(" ".join(sorted(expanded)), limit=max(limit * 3, 10))
        hits: list[RetrievalHit] = []
        original = set(re.findall(r"[a-zA-Z0-9_]{3,}", query.lower()))
        for item in candidates:
            matches = set(item.matched_terms)
            direct = len(matches & original)
            expanded_matches = len(matches)
            score = min(1.0, direct * 0.18 + expanded_matches * 0.05)
            if score <= 0:
                continue
            reason = "direct content match" if direct else "related concept match"
            hits.append(RetrievalHit(item.path, score, item.excerpt, tuple(sorted(matches)), reason))
        hits.sort(key=lambda hit: (-hit.score, hit.path))
        return tuple(hits[: max(1, limit)])

    @staticmethod
    def context(hits: tuple[RetrievalHit, ...], max_chars: int = 3000) -> str:
        if not hits:
            return ""
        lines = ["Local evidence:"]
        for index, hit in enumerate(hits, 1):
            lines.append(
                f"{index}. {hit.path} [{hit.reason}] — {hit.excerpt}"
            )
        return "\n".join(lines)[:max_chars]
