"""A17 verified planning boundary for WEBSTER.

Combines active goals, constraints, local evidence and registered tools into an
inspectable plan. Planning is deterministic and never executes a tool itself.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

from .planning_engine import Plan, PlanStep, PlanningEngine
from .multi_turn_reasoning import ReasoningContext
from .local_retrieval import RetrievalHit


@dataclass(frozen=True)
class VerifiedStep:
    index: int
    description: str
    depends_on: tuple[int, ...]
    capabilities: tuple[str, ...]
    executable: bool
    reason: str


@dataclass(frozen=True)
class VerifiedPlan:
    goal: str
    constraints: tuple[str, ...]
    evidence: tuple[str, ...]
    available_tools: tuple[str, ...]
    steps: tuple[VerifiedStep, ...]
    executable: bool
    blockers: tuple[str, ...]
    confidence: float

    @property
    def ready_steps(self) -> tuple[VerifiedStep, ...]:
        completed = set()
        return tuple(
            step for step in self.steps
            if step.executable and all(dep in completed for dep in step.depends_on)
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "goal": self.goal,
            "constraints": list(self.constraints),
            "evidence": list(self.evidence),
            "available_tools": list(self.available_tools),
            "steps": [
                {
                    "index": step.index,
                    "description": step.description,
                    "depends_on": list(step.depends_on),
                    "capabilities": list(step.capabilities),
                    "executable": step.executable,
                    "reason": step.reason,
                }
                for step in self.steps
            ],
            "executable": self.executable,
            "blockers": list(self.blockers),
            "confidence": self.confidence,
        }


class RobustPlanner:
    """Build and verify plans without bypassing the normal action/tool boundary."""

    _CAPABILITY_RULES = (
        (re.compile(r"\b(?:calculate|calc|compute|multiply|divide|add|subtract)\b", re.I), "local.compute"),
        (re.compile(r"\b(?:time|clock)\b", re.I), "runtime.read"),
        (re.compile(r"\b(?:file|files|document|documents|search)\b", re.I), "local.read"),
        (re.compile(r"\b(?:open|launch|start)\b", re.I), "desktop.execute"),
        (re.compile(r"\b(?:browser|website|web|url)\b", re.I), "browser.execute"),
        (re.compile(r"\b(?:camera|image|vision|screenshot)\b", re.I), "vision.read"),
    )

    def __init__(self, planner: PlanningEngine | None = None) -> None:
        self.planner = planner or PlanningEngine()

    def build(
        self,
        goal: str,
        *,
        context: ReasoningContext | None = None,
        evidence: Iterable[RetrievalHit] = (),
        available_tools: Iterable[str] = (),
    ) -> VerifiedPlan:
        clean_goal = " ".join(goal.split())[:2000]
        constraints = tuple(context.constraints[-8:]) if context else ()
        evidence_items = tuple(
            f"{hit.path}: {hit.excerpt}"[:700] for hit in list(evidence)[:6]
        )
        tools = tuple(sorted({str(name).strip().lower() for name in available_tools if str(name).strip()}))
        base = self.planner.create_plan(clean_goal)
        steps: list[VerifiedStep] = []
        blockers: list[str] = []

        for step in base.steps:
            capabilities = self._capabilities(step.description)
            missing = [cap for cap in capabilities if not self._capability_available(cap, tools)]
            executable = not missing
            reason = "all required capabilities are available" if executable else "missing capability: " + ", ".join(missing)
            if missing:
                blockers.extend(f"step {step.index}: {cap}" for cap in missing)
            steps.append(
                VerifiedStep(
                    step.index,
                    step.description,
                    step.depends_on,
                    tuple(capabilities),
                    executable,
                    reason,
                )
            )

        if not clean_goal:
            blockers.append("goal is empty")
        if not steps and clean_goal:
            blockers.append("no plan steps were produced")

        confidence = 1.0
        if blockers:
            confidence -= min(0.7, 0.15 * len(blockers))
        if not evidence_items and context and context.goal:
            confidence -= 0.05
        confidence = round(max(0.0, min(1.0, confidence)), 3)

        return VerifiedPlan(
            clean_goal,
            constraints,
            evidence_items,
            tools,
            tuple(steps),
            bool(steps) and not blockers,
            tuple(dict.fromkeys(blockers)),
            confidence,
        )

    @staticmethod
    def _capabilities(description: str) -> tuple[str, ...]:
        found: list[str] = []
        for pattern, capability in RobustPlanner._CAPABILITY_RULES:
            if pattern.search(description):
                found.append(capability)
        return tuple(dict.fromkeys(found))

    @staticmethod
    def _capability_available(capability: str, tools: tuple[str, ...]) -> bool:
        if capability == "local.compute":
            return "calculator" in tools
        if capability == "runtime.read":
            return "time" in tools
        # These capabilities are architecture boundaries; a missing concrete
        # tool means the step must not be called executable.
        return capability in tools
