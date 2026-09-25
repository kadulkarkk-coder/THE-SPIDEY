"""Small dependency-free knowledge graph for explicit relationships."""
from __future__ import annotations

class KnowledgeGraph:
    def __init__(self) -> None:
        self._edges: dict[str, set[tuple[str, str]]] = {}

    def add(self, subject: str, relation: str, object_: str) -> None:
        subject, relation, object_ = subject.strip(), relation.strip(), object_.strip()
        if not subject or not relation or not object_: raise ValueError("graph terms are required")
        self._edges.setdefault(subject, set()).add((relation, object_))

    def related(self, subject: str) -> tuple[tuple[str, str], ...]:
        return tuple(sorted(self._edges.get(subject.strip(), ())))

    def subjects(self) -> tuple[str, ...]:
        return tuple(sorted(self._edges))
