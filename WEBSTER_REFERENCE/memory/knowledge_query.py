"""Query helpers over the explicit knowledge graph."""
from __future__ import annotations
from .knowledge_graph import KnowledgeGraph

class KnowledgeQuery:
    def __init__(self, graph: KnowledgeGraph) -> None:
        self.graph = graph

    def relations(self, subject: str, relation: str | None = None) -> tuple[tuple[str, str], ...]:
        edges = self.graph.related(subject)
        if relation is None:
            return edges
        return tuple(edge for edge in edges if edge[0] == relation.strip())
