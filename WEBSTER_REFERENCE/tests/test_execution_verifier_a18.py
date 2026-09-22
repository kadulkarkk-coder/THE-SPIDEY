from WEBSTER_REFERENCE.intelligence.action_router import ActionResult
from WEBSTER_REFERENCE.intelligence.execution_verifier import ExecutionVerifier


def test_success_requires_observable_result() -> None:
    verifier = ExecutionVerifier()
    assert verifier.verify(ActionResult(True, True, "42", "calculator", "tool", {"tool": "calculator"})).ok
    assert not verifier.verify(ActionResult(True, True, "", "calculator", "tool", {"tool": "calculator"})).ok


def test_transient_failure_is_bounded_retryable() -> None:
    verifier = ExecutionVerifier()
    result = verifier.verify(ActionResult(True, False, "temporary timeout", "calculator", "tool"))
    assert result.retryable
    assert verifier.can_retry(result, 0)
    assert verifier.can_retry(result, 1)
    assert not verifier.can_retry(result, 2)


def test_not_handled_cannot_verify() -> None:
    assert not ExecutionVerifier().verify(ActionResult.not_handled()).ok
