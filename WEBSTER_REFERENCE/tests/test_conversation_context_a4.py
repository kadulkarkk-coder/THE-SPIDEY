"""A4 tests for bounded conversation context and structured responses."""
from __future__ import annotations

from WEBSTER_REFERENCE.intelligence.context_builder import ContextBuilder
from WEBSTER_REFERENCE.intelligence.conversation_state import ConversationState
from WEBSTER_REFERENCE.intelligence.decision_engine import DecisionEngine
from WEBSTER_REFERENCE.intelligence.response_composer import ResponseComposer


def test_conversation_state_is_bounded() -> None:
    state = ConversationState(max_turns=3, max_chars_per_turn=10)
    for index in range(5):
        state.add("user", f"message-{index}-extra")
    turns = state.recent()
    assert len(turns) == 3
    assert turns[0].text == "message-2-"


def test_context_contains_recent_turns() -> None:
    state = ConversationState(max_turns=4)
    state.add("user", "My project is WEBSTER")
    state.add("assistant", "Understood")
    context = ContextBuilder().build("What is my project?", state, {"state": "running"})
    rendered = ContextBuilder.as_prompt(context)
    assert "Current request: What is my project?" in rendered
    assert "user: My project is WEBSTER" in rendered
    assert context.runtime["state"] == "running"


def test_local_provider_can_use_context_for_last_message() -> None:
    state = ConversationState()
    state.add("user", "hello WEBSTER")
    state.add("assistant", "Hello!")
    state.add("user", "what did I say?")
    prompt = ContextBuilder.as_prompt(ContextBuilder().build("what did I say?", state))
    decision = DecisionEngine().decide(prompt)
    assert decision.provider == "local"
    assert "what did I say?" in decision.rationale.lower()


def test_response_composer_preserves_decision_metadata() -> None:
    decision = DecisionEngine().decide("calculate 12 * 7")
    response = ResponseComposer().compose(decision)
    assert response.text == "The answer is 84."
    assert response.provider == "local"
    assert response.action == "respond"
