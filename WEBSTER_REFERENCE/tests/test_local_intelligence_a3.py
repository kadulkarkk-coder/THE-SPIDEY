"""A3 tests for dependency-free local intelligence."""
from intelligence.decision_engine import DecisionEngine, OfflineProvider
from intelligence.local_calculator import calculate
from intelligence.local_provider import LocalProvider


def test_local_provider_is_default() -> None:
    assert DecisionEngine().provider.name == "local"


def test_local_provider_answers_identity() -> None:
    response = LocalProvider().generate("Who are you?")
    assert response.provider == "local"
    assert "WEBSTER" in response.text


def test_local_provider_calculates() -> None:
    response = LocalProvider().generate("calculate 12 * 7")
    assert response.text == "The answer is 84."
    assert response.confidence > 0.9


def test_calculator_rejects_code() -> None:
    assert calculate("__import__('os').system('whoami')") is None


def test_external_style_provider_remains_replaceable() -> None:
    engine = DecisionEngine(OfflineProvider())
    assert engine.provider.name == "offline"
