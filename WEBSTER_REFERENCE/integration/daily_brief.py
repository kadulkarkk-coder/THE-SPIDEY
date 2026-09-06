"""Deterministic Daily Brief aggregation for WEBSTER clients."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DailyBrief:
    date: str
    priorities: tuple[str, ...] = field(default_factory=tuple)
    study_task: str = ""
    pending_tasks: tuple[str, ...] = field(default_factory=tuple)
    reminders: tuple[str, ...] = field(default_factory=tuple)
    suggestion: str = ""


class DailyBriefBuilder:
    def build(self, date: str, *, priorities=(), study_task: str = "", pending_tasks=(), reminders=(), suggestion: str = "") -> DailyBrief:
        if not date.strip():
            raise ValueError("date must not be empty")
        return DailyBrief(date, tuple(priorities), study_task, tuple(pending_tasks), tuple(reminders), suggestion)
