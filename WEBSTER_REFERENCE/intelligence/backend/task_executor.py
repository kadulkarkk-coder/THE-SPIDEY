"""Deterministic multi-step task execution for WEBSTER A7."""
from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4
from .planning_engine import Plan, PlanningEngine
from .progress_reporter import ProgressReporter
from .action_router import ActionRouter, ActionResult
from .task_memory import TaskMemoryStore
from .execution_verifier import ExecutionVerifier, VerificationResult
from .execution_audit import ExecutionAuditor
from .reliability_checker import ReliabilityChecker
from .self_correction import SelfCorrection

@dataclass(frozen=True)
class TaskExecutionResult:
    task_id: str
    ok: bool
    plan: Plan
    results: tuple[ActionResult, ...]
    error: str = ""

class TaskExecutor:
    """Executes only ready plan steps, stopping safely on the first failure."""

    def __init__(self, planner: PlanningEngine, router: ActionRouter, progress: ProgressReporter, memory: TaskMemoryStore | None = None, verifier: ExecutionVerifier | None = None) -> None:
        self.planner = planner
        self.router = router
        self.progress = progress
        self.memory = memory
        self.verifier = verifier or ExecutionVerifier()
        self.auditor = ExecutionAuditor()
        self.reliability = ReliabilityChecker()
        self.self_correction = SelfCorrection()

    def execute(self, goal: str, *, task_id: str | None = None, session_id: str = "") -> TaskExecutionResult:
        task_id = task_id or uuid4().hex
        plan = self.planner.create_plan(goal)
        if not plan.steps:
            self.progress.report(task_id, "failed", 0.0, "No executable plan was created.")
            result = TaskExecutionResult(task_id, False, plan, (), "empty plan")
            if self.memory: self.memory.remember(task_id, goal, "failed", error=result.error, session_id=session_id)
            return result

        self.progress.report(task_id, "started", 0.0, f"Executing {len(plan.steps)} step(s).")
        results: list[ActionResult] = []
        verifications: list[VerificationResult] = []
        for step in plan.steps:
            ready = self.planner.next_ready(plan)
            if step not in ready:
                plan = self.planner.mark_step(plan, step.index, "failed")
                self.progress.report(task_id, "failed", plan.progress, f"Dependency for step {step.index} was not satisfied.")
                result = TaskExecutionResult(task_id, False, plan, tuple(results), "dependency not satisfied")
                if self.memory: self.memory.remember(task_id, goal, "failed", [x.message for x in results], result.error, session_id)
                return result

            plan = self.planner.mark_step(plan, step.index, "active")
            self.progress.report(task_id, "active", plan.progress, f"Step {step.index}: {step.description}")
            action = self.router.route(
                self.router_input(step.description),
                request_id=task_id,
            )
            verification = self.verifier.verify(action)
            attempts = 1
            while not verification.ok:
                audit_preview = self.auditor.record(task_id, plan, step.index, action, verification)
                decision = self.self_correction.decide(verification, audit_preview, attempts=attempts)
                if decision.action != "retry":
                    break
                self.progress.report(task_id, "recovering", plan.progress, decision.user_message)
                action = self.router.route(
                    self.router_input(step.description),
                    request_id=task_id,
                )
                verification = self.verifier.verify(action)
                attempts += 1
            results.append(action)
            verifications.append(verification)
            audit = self.auditor.record(task_id, plan, step.index, action, verification)
            if not verification.ok:
                plan = self.planner.mark_step(plan, step.index, "failed")
                decision = self.self_correction.decide(verification, audit, attempts=attempts)
                message = f"Step {step.index} stopped safely: {decision.user_message}"
                self.progress.report(task_id, "failed", plan.progress, message)
                result = TaskExecutionResult(task_id, False, plan, tuple(results), message)
                if self.memory: self.memory.remember(task_id, goal, "failed", [x.message for x in results], result.error, session_id)
                return result
            plan = self.planner.mark_step(plan, step.index, "completed")
            self.progress.report(task_id, "active", plan.progress, f"Step {step.index} verified and completed.")

        consistency = self.reliability.check(plan, tuple(results), tuple(verifications))
        if not consistency.ok:
            self.progress.report(task_id, "failed", plan.progress, f"Reliability check failed: {consistency.reason}")
            result = TaskExecutionResult(task_id, False, plan, tuple(results), consistency.reason)
            if self.memory: self.memory.remember(task_id, goal, "failed", [x.message for x in results], result.error, session_id)
            return result
        self.progress.report(task_id, "completed", 1.0, "All planned steps completed and passed reliability checks.")
        result = TaskExecutionResult(task_id, True, plan, tuple(results))
        if self.memory: self.memory.remember(task_id, goal, "completed", [x.message for x in results], session_id=session_id)
        return result

    @staticmethod
    def router_input(description: str):
        from .intent_pipeline import IntelligencePipeline
        return IntelligencePipeline().interpret(description)
