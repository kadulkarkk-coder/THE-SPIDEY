"""WEBSTER application runtime with a functional lifecycle boundary."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .command_contracts import CommandRequest, CommandResponse
from .command_dispatcher import CommandDispatcher
from .component_registry import ComponentRegistry
from .config import WebsterConfig
from .diagnostics import Diagnostics
from .event_bus import EventBus
from .health_monitor import HealthMonitor
from .lifecycle import LifecycleManager, LifecycleState
from .request_pipeline import RequestPipeline
from .runtime_context import RuntimeContext
from .service_registry import ServiceRegistry
from ..intelligence.context_builder import ContextBuilder
from ..intelligence.conversation_manager import ConversationManager
from ..intelligence.conversation_state import ConversationState
from ..intelligence.decision_engine import DecisionEngine
from ..intelligence.planning_engine import PlanningEngine
from ..intelligence.progress_reporter import ProgressReporter
from ..intelligence.response_composer import ResponseComposer
from ..runtime.request_bridge import RuntimeRequestBridge
from ..runtime.runtime_manager import RuntimeManager


class WebsterApplication:
    """Functional WEBSTER runtime facade shared by desktop and packaged clients."""

    VERSION = "0.2.0-alpha"

    def __init__(self, config: WebsterConfig | None = None) -> None:
        self.config = config or WebsterConfig.from_environment()
        self.events = EventBus()
        self.health = HealthMonitor()
        self.lifecycle = LifecycleManager()
        self.components = ComponentRegistry()
        self.services = ServiceRegistry()
        self.diagnostics = Diagnostics()
        self.context = RuntimeContext(session_id=uuid4().hex)
        self.commands = CommandDispatcher()
        self.pipeline = RequestPipeline(self.commands, self.diagnostics)
        self.conversation = ConversationManager()
        self.conversation_state = ConversationState()
        self.context_builder = ContextBuilder()
        self.response_composer = ResponseComposer()
        self.decision_engine = DecisionEngine()
        self.planning = PlanningEngine()
        self.progress = ProgressReporter()
        self.runtime = RuntimeManager()
        self.request_bridge = RuntimeRequestBridge(self.pipeline, self.runtime, self.events)
        self.started_at: datetime | None = None
        self._register_core_components()
        self._register_intelligence_services()
        self._register_commands()

    def _register_core_components(self) -> None:
        self.health.register("event_bus")
        self.health.register("health_monitor")
        self.health.register("lifecycle")
        self.health.register("command_dispatcher")
        self.health.register("request_pipeline")
        self.health.register("runtime_request_bridge")
        self.components.register("event_bus", self.events, "In-process event bus")
        self.components.register("health_monitor", self.health, "Runtime health state")
        self.components.register("lifecycle", self.lifecycle, "Application lifecycle")
        self.components.register("command_dispatcher", self.commands, "Command routing")
        self.components.register("request_pipeline", self.pipeline, "Unified request processing")
        self.components.register("runtime", self.runtime, "Functional service lifecycle")
        self.components.register("runtime_request_bridge", self.request_bridge, "Single client request boundary")
        self.services.register_service("diagnostics", self.diagnostics, "Runtime metrics")

    def _register_intelligence_services(self) -> None:
        self.services.register_service("conversation", self.conversation, "Bounded conversation state")
        self.services.register_service("conversation_state", self.conversation_state, "Bounded contextual session state")
        self.services.register_service("context_builder", self.context_builder, "Bounded request context")
        self.services.register_service("response_composer", self.response_composer, "Structured response composition")
        self.services.register_service("decision_engine", self.decision_engine, "Provider-backed decision boundary")
        self.services.register_service("planning", self.planning, "Explicit plan decomposition")
        self.services.register_service("progress", self.progress, "Observable task progress")

    def _register_commands(self) -> None:
        self.commands.register("help", self._command_help)
        self.commands.register("status", self._command_status)
        self.commands.register("diagnostics", self._command_diagnostics)
        self.commands.register("context", self._command_context)
        self.commands.register("runtime", self._command_runtime)
        self.commands.register("ai", self._command_ai)
        self.commands.register("plan", self._command_plan)
        self.commands.register("exit", self._command_exit)
        self.commands.register("quit", self._command_exit)

    def start(self) -> None:
        if self.lifecycle.state is LifecycleState.RUNNING:
            return
        try:
            self.lifecycle.start()
            self.runtime.start()
            self.started_at = datetime.now(timezone.utc)
            self.events.publish("system.started", {"version": self.VERSION, "session_id": self.context.session_id})
        except Exception as exc:
            self.lifecycle.fail()
            self.health.set_status("lifecycle", "failed", healthy=False, detail=str(exc))
            raise

    def stop(self) -> None:
        if self.lifecycle.state is not LifecycleState.RUNNING:
            return
        self.events.publish("system.stopping")
        self.runtime.stop()
        self.lifecycle.stop()
        self.events.publish("system.stopped")

    def status(self) -> dict[str, Any]:
        return {
            "name": self.config.name,
            "version": self.VERSION,
            "environment": self.config.environment,
            "running": self.lifecycle.state is LifecycleState.RUNNING,
            "state": self.lifecycle.state.value,
            "runtime_state": self.runtime.state.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "components": self.health.component_count,
            "commands": self.commands.count(),
            "services": 12,
            "provider": self.decision_engine.provider.name,
            "conversation_turns": self.conversation_state.size(),
            "healthy": self.health.is_healthy(),
        }

    def handle(self, request: CommandRequest) -> CommandResponse:
        """Run one request through the single runtime request boundary."""
        return self.request_bridge.submit(request)

    def command(self, text: str) -> str:
        """Backward-compatible text command API for the CLI."""
        response = self.handle(CommandRequest(text))
        if response.ok:
            return response.message
        return f"Error [{response.error_code}]: {response.message}"

    def _command_help(self, request: CommandRequest) -> str:
        return "Available commands: " + ", ".join(self.commands.names())

    def _command_status(self, request: CommandRequest) -> str:
        return str(self.status())

    def _command_diagnostics(self, request: CommandRequest) -> str:
        return str(self.diagnostics.as_dict())

    def _command_context(self, request: CommandRequest) -> str:
        return str(self.context.snapshot())

    def _command_runtime(self, request: CommandRequest) -> str:
        return str(self.runtime.snapshot())

    def _command_ai(self, request: CommandRequest) -> str:
        parts = request.text.split(maxsplit=1)
        prompt = parts[1] if len(parts) > 1 else ""
        current = prompt or request.text
        self.conversation.add("user", current)
        self.conversation_state.add("user", current)
        built = self.context_builder.build(current, self.conversation_state, self.runtime.snapshot().__dict__)
        decision = self.decision_engine.decide(self.context_builder.as_prompt(built))
        composed = self.response_composer.compose(decision)
        self.conversation.add("assistant", composed.text)
        self.conversation_state.add("assistant", composed.text)
        self.events.publish("intelligence.response.composed", {
            "provider": composed.provider,
            "confidence": composed.confidence,
            "requires_review": composed.requires_review,
        })
        return composed.text

    def _command_plan(self, request: CommandRequest) -> str:
        parts = request.text.split(maxsplit=1)
        goal = parts[1] if len(parts) > 1 else ""
        plan = self.planning.create_plan(goal)
        return str({"goal": plan.goal, "steps": [step.description for step in plan.steps]})

    def _command_exit(self, request: CommandRequest) -> str:
        self.stop()
        return "WEBSTER stopped."
