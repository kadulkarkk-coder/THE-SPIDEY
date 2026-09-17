"""WEBSTER intelligence services: local-first with optional provider adapters."""

from .decision_engine import Decision, DecisionEngine, OfflineProvider, ProviderResponse
from .local_calculator import calculate
from .local_knowledge import LocalKnowledge
from .local_provider import LocalProvider

__all__ = [
    "Decision", "DecisionEngine", "OfflineProvider", "ProviderResponse",
    "LocalProvider", "LocalKnowledge", "calculate",
]
