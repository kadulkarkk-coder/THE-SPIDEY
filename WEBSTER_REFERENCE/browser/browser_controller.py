"""High-level browser capability coordinator; concrete browser drivers remain optional."""
from __future__ import annotations
from .browser_permissions import BrowserPermissions
from .browser_observer import BrowserObserver
from .navigation import NavigationPlanner

class BrowserController:
    def __init__(self, permissions=None, observer=None, planner=None) -> None:
        self.permissions = permissions or BrowserPermissions(); self.observer = observer or BrowserObserver(); self.planner = planner or NavigationPlanner()
    def plan_navigation(self, principal: str, url: str):
        if not self.permissions.allowed(principal, "navigate"): raise PermissionError("browser navigation is not permitted")
        plan = self.planner.plan(url); self.observer.record("navigate", plan.url, True, "planned"); return plan
