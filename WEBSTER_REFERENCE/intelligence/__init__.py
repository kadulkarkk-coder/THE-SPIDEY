"""WEBSTER intelligence services: local-first with optional provider adapters."""

from .context_builder import BuiltContext, ContextBuilder
from .conversation_state import ConversationState, ConversationTurn
from .decision_engine import Decision, DecisionEngine, OfflineProvider, ProviderResponse
from .local_calculator import calculate
from .local_knowledge import LocalKnowledge
from .local_provider import LocalProvider
from .response_composer import ComposedResponse, ResponseComposer

__all__ = [
    "Decision", "DecisionEngine", "OfflineProvider", "ProviderResponse",
    "LocalProvider", "LocalKnowledge", "calculate",
    "ConversationState", "ConversationTurn", "ContextBuilder", "BuiltContext",
    "ResponseComposer", "ComposedResponse",
]
