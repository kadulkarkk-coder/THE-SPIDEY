"""A5 tests for functional intent/reasoning routing."""
from WEBSTER_REFERENCE.intelligence.intent_pipeline import IntelligencePipeline
from WEBSTER_REFERENCE.intelligence.intent_router import IntentRouter


def test_question_is_routed_to_knowledge() -> None:
    result = IntelligencePipeline().interpret("What is WEBSTER?")
    assert result.intent == "question"
    assert result.target == "knowledge"
    assert result.confidence > 0


def test_url_and_number_entities_are_extracted() -> None:
    result = IntelligencePipeline().interpret("open https://example.com at 42")
    kinds = {entity["kind"] for entity in result.entities}
    assert {"url", "number"}.issubset(kinds)


def test_constraints_can_block_a_route() -> None:
    from WEBSTER_REFERENCE.intelligence.constraint_engine import Constraint
    result = IntelligencePipeline().interpret(
        "do something", constraints=[Constraint("blocked", lambda _: False)]
    )
    assert not result.constraints_allowed
    assert result.failed_constraints == ("blocked",)


def test_router_returns_explicit_reason() -> None:
    _, route = IntentRouter().route("hello WEBSTER")
    assert route.target == "conversation"
    assert "hello" in route.reason
