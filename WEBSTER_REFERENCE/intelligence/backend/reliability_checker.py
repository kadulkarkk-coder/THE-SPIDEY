"""A19 plan/result consistency checks for WEBSTER."""
from __future__ import annotations
from dataclasses import dataclass
from .planning_engine import Plan
from .action_router import ActionResult
from .execution_verifier import VerificationResult


@dataclass(frozen=True)
class ReliabilityCheck:
    ok: bool
    status: str
    reason: str


class ReliabilityChecker:
    """Prevents a task from being reported complete when its plan/results disagree."""

    def check(self, plan: Plan, results: tuple[ActionResult, ...], verifications: tuple[VerificationResult, ...]) -> ReliabilityCheck:
        if len(results) != len(verifications):
            return ReliabilityCheck(False, "result_mismatch", "Every action result must have a matching verification.")
        if any(not item.ok for item in verifications):
            return ReliabilityCheck(False, "unverified_step", "At least one executed step failed verification.")
        completed = {step.index for step in plan.steps if step.status == "completed"}
        expected = {step.index for step in plan.steps}
        if completed != expected:
            return ReliabilityCheck(False, "plan_incomplete", "The plan contains steps that are not completed.")
        if len(results) != len(plan.steps):
            return ReliabilityCheck(False, "step_count_mismatch", "The number of executed results does not match the plan.")
        return ReliabilityCheck(True, "consistent", "Plan, execution results, and verification records agree.")
