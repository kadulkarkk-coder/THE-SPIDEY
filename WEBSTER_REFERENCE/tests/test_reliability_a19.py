from WEBSTER_REFERENCE.intelligence.action_router import ActionResult
from WEBSTER_REFERENCE.intelligence.execution_verifier import ExecutionVerifier
from WEBSTER_REFERENCE.intelligence.execution_audit import ExecutionAuditor
from WEBSTER_REFERENCE.intelligence.planning_engine import PlanningEngine
from WEBSTER_REFERENCE.intelligence.reliability_checker import ReliabilityChecker


def test_audit_classifies_false_success() -> None:
    action = ActionResult(True, True, "", "calculator", "tool", {"tool": "calculator"})
    verification = ExecutionVerifier().verify(action)
    assert ExecutionAuditor.classify(action, verification) == "false_success"


def test_consistency_rejects_missing_verification() -> None:
    plan = PlanningEngine().create_plan("calculate 2 + 2")
    action = ActionResult(True, True, "4", "calculator", "tool", {"tool": "calculator"})
    check = ReliabilityChecker().check(plan, (action,), ())
    assert not check.ok
    assert check.status == "result_mismatch"
