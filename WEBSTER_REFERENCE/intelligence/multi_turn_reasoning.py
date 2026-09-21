"""A15 bounded multi-turn reasoning context for WEBSTER.

Keeps goals, entities, constraints, results and recent decisions together while
remaining session-local, size-bounded and deterministic.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from time import monotonic
import re


@dataclass(frozen=True)
class ReasoningTurn:
    turn: int
    role: str
    text: str
    task_id: str = ""


@dataclass
class ReasoningContext:
    session_id: str
    max_turns: int = 24
    max_items: int = 32
    ttl_seconds: float = 1800.0
    turns: list[ReasoningTurn] = field(default_factory=list)
    goal: str = ""
    entities: dict[str, str] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
    results: list[str] = field(default_factory=list)
    task_ids: list[str] = field(default_factory=list)
    last_intent: str = ""
    last_target: str = ""
    updated_at: float = field(default_factory=monotonic)

    def add_turn(self, role: str, text: str, task_id: str = "") -> None:
        self._expire()
        cleaned = " ".join(text.split())[:1200]
        if not cleaned:
            return
        self.turns.append(ReasoningTurn(len(self.turns) + 1, role.strip().lower(), cleaned, task_id))
        self.turns = self.turns[-self.max_turns:]
        if task_id and task_id not in self.task_ids:
            self.task_ids.append(task_id)
            self.task_ids = self.task_ids[-self.max_items:]
        self.updated_at = monotonic()

    def set_goal(self, goal: str) -> None:
        goal = " ".join(goal.split())[:1000]
        if goal:
            self.goal = goal
            self.updated_at = monotonic()

    def set_entities(self, entities: dict[str, str]) -> None:
        for key, value in list(entities.items())[:self.max_items]:
            self.entities[str(key)] = str(value)[:500]
        self.entities = dict(list(self.entities.items())[-self.max_items:])
        self.updated_at = monotonic()

    def set_constraints(self, constraints: list[str] | tuple[str, ...]) -> None:
        clean = [" ".join(str(x).split())[:400] for x in constraints if str(x).strip()]
        self.constraints = list(dict.fromkeys(clean))[-self.max_items:]
        self.updated_at = monotonic()

    def set_results(self, results: list[str] | tuple[str, ...]) -> None:
        self.results = [str(x)[:700] for x in results][-10:]
        self.updated_at = monotonic()

    def resolve(self, phrase: str) -> str | None:
        self._expire()
        key = " ".join(phrase.lower().strip().split())
        aliases = {
            "the goal": self.goal,
            "our goal": self.goal,
            "the task": self.goal,
            "that task": self.goal,
            "this task": self.goal,
            "the last result": self.results[-1] if self.results else "",
            "the previous result": self.results[-2] if len(self.results) > 1 else "",
            "the last task": self.task_ids[-1] if self.task_ids else "",
        }
        if key in aliases and aliases[key]:
            return aliases[key]
        if key.startswith("the ") and key[4:] in self.entities:
            return self.entities[key[4:]]
        return self.entities.get(key)

    def summary(self) -> dict[str, object]:
        self._expire()
        return {
            "session_id": self.session_id,
            "goal": self.goal,
            "entities": dict(self.entities),
            "constraints": list(self.constraints),
            "results": list(self.results),
            "task_ids": list(self.task_ids),
            "last_intent": self.last_intent,
            "last_target": self.last_target,
            "turn_count": len(self.turns),
        }

    def prompt_context(self, max_chars: int = 2600) -> str:
        self._expire()
        lines = []
        if self.goal:
            lines.append("Active goal: " + self.goal)
        if self.entities:
            lines.append("Relevant entities: " + ", ".join(f"{k}={v}" for k, v in self.entities.items()))
        if self.constraints:
            lines.append("Constraints: " + "; ".join(self.constraints))
        if self.results:
            lines.append("Recent results: " + "; ".join(self.results[-4:]))
        if self.turns:
            lines.append("Recent reasoning turns:")
            lines.extend(f"{t.role}: {t.text}" for t in self.turns[-8:])
        return "\n".join(lines)[:max_chars]

    def _expire(self) -> None:
        if monotonic() - self.updated_at > self.ttl_seconds:
            self.turns.clear()
            self.entities.clear()
            self.constraints.clear()
            self.results.clear()
            self.task_ids.clear()
            self.goal = ""
            self.last_intent = ""
            self.last_target = ""
            self.updated_at = monotonic()


class MultiTurnReasoning:
    """Session-local manager; never mixes contexts from different sessions."""

    def __init__(self, max_sessions: int = 8) -> None:
        self.max_sessions = max(1, max_sessions)
        self._contexts: dict[str, ReasoningContext] = {}

    def context(self, session_id: str) -> ReasoningContext:
        if not session_id:
            raise ValueError("session_id is required")
        ctx = self._contexts.get(session_id)
        if ctx is None:
            ctx = ReasoningContext(session_id=session_id)
            self._contexts[session_id] = ctx
            if len(self._contexts) > self.max_sessions:
                oldest = min(self._contexts, key=lambda sid: self._contexts[sid].updated_at)
                self._contexts.pop(oldest, None)
        return ctx

    def observe(
        self,
        session_id: str,
        *,
        role: str,
        text: str,
        task_id: str = "",
        intent: str = "",
        target: str = "",
        goal: str = "",
        entities: dict[str, str] | None = None,
        constraints: list[str] | None = None,
        results: list[str] | None = None,
    ) -> ReasoningContext:
        ctx = self.context(session_id)
        ctx.add_turn(role, text, task_id)
        if goal:
            ctx.set_goal(goal)
        if entities:
            ctx.set_entities(entities)
        if constraints:
            ctx.set_constraints(constraints)
        if results:
            ctx.set_results(results)
        if intent:
            ctx.last_intent = intent
        if target:
            ctx.last_target = target
        return ctx

    def prompt_context(self, session_id: str) -> str:
        return self.context(session_id).prompt_context()

    def snapshot(self, session_id: str) -> dict[str, object]:
        return self.context(session_id).summary()
