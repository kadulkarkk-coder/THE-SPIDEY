"""Navigation planning boundary for browser agents."""
from __future__ import annotations
from dataclasses import dataclass
from .url_policy import URLPolicy

@dataclass(frozen=True)
class NavigationPlan:
    url: str
    action: str = "navigate"

class NavigationPlanner:
    def __init__(self, policy: URLPolicy | None = None) -> None: self.policy = policy or URLPolicy()
    def plan(self, url: str) -> NavigationPlan:
        return NavigationPlan(self.policy.require_valid(url))
