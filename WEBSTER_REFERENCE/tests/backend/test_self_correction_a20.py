from WEBSTER_REFERENCE.intelligence.execution_verifier import VerificationResult
from WEBSTER_REFERENCE.intelligence.self_correction import SelfCorrection


def test_transient_failure_requests_bounded_retry() -> None:
    decision = SelfCorrection().decide(
        VerificationResult(False, "failed", "temporary timeout", True),
        attempts=1,
    )
    assert decision.action == "retry"


def test_unverifiable_success_stops_safely() -> None:
    decision = SelfCorrection().decide(
        VerificationResult(False, "no_observable_result", "no result"),
        attempts=1,
    )
    assert decision.action == "stop"
    assert "verified" in decision.user_message


def test_verified_result_is_accepted() -> None:
    decision = SelfCorrection().decide(
        VerificationResult(True, "verified", "ok"),
    )
    assert decision.action == "accept"
