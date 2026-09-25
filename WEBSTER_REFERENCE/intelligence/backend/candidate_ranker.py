"""Candidate ranking for WEBSTER answer/action alternatives."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Candidate:
    value: str
    score: float

class CandidateRanker:
    def rank(self, candidates: list[Candidate] | tuple[Candidate, ...]) -> tuple[Candidate, ...]:
        return tuple(sorted(candidates, key=lambda item: (-item.score, item.value)))
