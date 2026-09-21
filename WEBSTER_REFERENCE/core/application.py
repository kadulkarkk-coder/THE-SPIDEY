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
from ..intelligence.intent_pipeline import IntelligencePipeline
from ..intelligence.action_router import ActionRouter
from ..intelligence.local_calculator import calculate
from ..tools.tool_contract import ToolBinding, ToolSpec
from ..tools.tool_dispatcher import ToolDispatcher
from ..tools.tool_registry import ToolRegistry
from ..intelligence.planning_engine import PlanningEngine
from ..intelligence.progress_reporter import ProgressReporter
from ..intelligence.task_executor import TaskExecutor
from ..intelligence.task_memory import TaskMemoryStore
from ..intelligence.conversation_memory import ConversationMemoryStore
from ..intelligence.memory_reference_resolver import MemoryReferenceResolver
from ..intelligence.conversation_continuity import ConversationContinuity
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
        self.intelligence = IntelligencePipeline()
        self.response_composer = ResponseComposer()
        self.decision_engine = DecisionEngine()
        self.planning = PlanningEngine()
        self.tool_registry = ToolRegistry()
        self.tool_dispatcher = ToolDispatcher(self.tool_registry)
        self.action_router = ActionRouter(command_handler=self._action_command, tool_dispatcher=self.tool_dispatcher)
        self.progress = ProgressReporter()
        self.task_memory = TaskMemoryStore()
        self.conversation_memory = ConversationMemoryStore()
        self.reference_resolver = MemoryReferenceResolver(self.task_memory, self.conversation_memory)
        self.continuity = ConversationContinuity(self.task_memory)
        self.task_executor = TaskExecutor(self.planning, self.action_router, self.progress, self.task_memory)
        self.runtime = RuntimeManager()
        self.request_bridge = RuntimeRequestBridge(self.pipeline, self.runtime, self.events)
        self.started_at: datetime | None = None
        self._register_core_components()
        self._register_intelligence_services()
        self._register_action_tools()
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
        self.services.register_service("intelligence", self.intelligence, "Intent, entity, reasoning and constraint pipeline")
        self.services.register_service("response_composer", self.response_composer, "Structured response composition")
        self.services.register_service("decision_engine", self.decision_engine, "Local-first decision boundary")
        self.services.register_service("planning", self.planning, "Explicit plan decomposition")
        self.services.register_service("progress", self.progress, "Observable task progress")
        self.services.register_service("tool_dispatcher", self.tool_dispatcher, "Registered executable tools")
        self.services.register_service("action_router", self.action_router, "Intent-to-action routing")
        self.services.register_service("task_executor", self.task_executor, "Verified multi-step task execution")
        self.services.register_service("task_memory", self.task_memory, "Persistent local task outcomes")
        self.services.register_service("conversation_memory", self.conversation_memory, "Persistent local conversation recall")
        self.services.register_service("reference_resolver", self.reference_resolver, "Session-scoped memory reference resolution")
        self.services.register_service("continuity", self.continuity, "Reference-aware follow-up continuity")

    def _register_action_tools(self) -> None:
        from datetime import datetime

        self.tool_registry.register(
            ToolBinding(
                ToolSpec("calculator", "Safe local arithmetic", frozenset({"local.compute"})),
                calculate,
            )
        )
        self.tool_registry.register(
            ToolBinding(
                ToolSpec("time", "Current local time", frozenset({"runtime.read"})),
                lambda: datetime.now().astimezone().strftime("%H:%M:%S"),
            )
        )

    def _action_command(self, name: str) -> str:
        if name == "help":
            return self._command_help(CommandRequest("help"))
        if name == "status":
            return self._command_status(CommandRequest("status"))
        return "Unsupported action command."

    def _register_commands(self) -> None:
        self.commands.register("help", self._command_help)
        self.commands.register("status", self._command_status)
        self.commands.register("diagnostics", self._command_diagnostics)
        self.commands.register("context", self._command_context)
        self.commands.register("runtime", self._command_runtime)
        self.commands.register("ai", self._command_ai)
        self.commands.register("plan", self._command_plan)
        self.commands.register("run", self._command_run)
        self.commands.register("memory", self._command_memory)
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
            "services": 20,
            "provider": self.decision_engine.provider.name,
            "conversation_turns": self.conversation_state.size(),
            "healthy": self.health.is_healthy(),
        }

    def handle(self, request: CommandRequest) -> CommandResponse:
        return self.request_bridge.submit(request)

    def command(self, text: str) -> str:
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
        self.conversation_memory.remember(self.context.session_id, "user", current)
        memory_context = self.task_memory.summary(current, self.context.session_id)
        conversation_context = self.conversation_memory.context(current, self.context.session_id)
        built = self.context_builder.build(current, self.conversation_state, self.runtime.snapshot().as_dict())
        interpretation = self.intelligence.interpret(current)
        reference = self.reference_resolver.resolve(current, self.context.session_id)
        continuity = self.continuity.resolve(current, self.context.session_id)
        if continuity.resolved and continuity.intent == "recall_result":
            response_text = "The result was: " + continuity.text
            self.conversation.add("assistant", response_text)
            self.conversation_state.add("assistant", response_text)
            self.conversation_memory.remember(self.context.session_id, "assistant", response_text)
            return response_text
        if continuity.resolved and continuity.intent == "followup_calculation":
            result = self.task_executor.execute("calculate " + continuity.text, task_id=request.request_id or None, session_id=self.context.session_id)
            response_text = str({"task_id": result.task_id, "status": "completed" if result.ok else "failed", "results": [item.message for item in result.results], "error": result.error or None, "referenced_task_id": continuity.source_task_id})
            self.conversation.add("assistant", response_text)
            self.conversation_state.add("assistant", response_text)
            self.conversation_memory.remember(self.context.session_id, "assistant", response_text)
            return response_text
        if reference.intent == "clarify_task":
            options = [f"{index}. {item.goal}" for index, item in enumerate(reference.candidates, 1)]
            response_text = "I found multiple plausible previous tasks. Which one do you mean? " + " | ".join(options)
            self.conversation.add("assistant", response_text)
            self.conversation_state.add("assistant", response_text)
            self.conversation_memory.remember(self.context.session_id, "assistant", response_text)
            self.events.publish("memory.reference.clarification", {"candidates": [item.task_id for item in reference.candidates], "confidence": reference.confidence})
            return response_text
        if reference.resolved and reference.intent == "recall_task":
            response_text = "Earlier, the task was: " + reference.goal
            self.conversation.add("assistant", response_text)
            self.conversation_state.add("assistant", response_text)
            self.conversation_memory.remember(self.context.session_id, "assistant", response_text)
            return response_text
        if reference.resolved and reference.intent == "recall_conversation":
            response_text = "I found this relevant earlier conversation: " + reference.goal
            self.conversation.add("assistant", response_text)
            self.conversation_state.add("assistant", response_text)
            self.conversation_memory.remember(self.context.session_id, "assistant", response_text)
            return response_text
        if reference.resolved and reference.intent in {"repeat_task", "continue_task"}:
            task = self.task_executor.execute(reference.goal, task_id=request.request_id or None, session_id=self.context.session_id)
            response_text = str({"task_id": task.task_id, "status": "completed" if task.ok else "failed", "referenced_task_id": reference.task_id, "intent": reference.intent, "results": [item.message for item in task.results], "error": task.error or None})
            self.conversation.add("assistant", response_text)
            self.conversation_state.add("assistant", response_text)
            self.conversation_memory.remember(self.context.session_id, "assistant", response_text)
            return response_text
        if " then " in current.lower():
            task = self.task_executor.execute(current, task_id=request.request_id or None, session_id=self.context.session_id)
            response_text = str({"task_id": task.task_id, "status": "completed" if task.ok else "failed", "results": [item.message for item in task.results], "error": task.error or None})
            self.conversation.add("assistant", response_text)
            self.conversation_state.add("assistant", response_text)
            self.conversation_memory.remember(self.context.session_id, "assistant", response_text)
            self.events.publish("intelligence.interpreted", interpretation.as_dict())
            self.events.publish("task.completed" if task.ok else "task.failed", {"task_id": task.task_id, "steps": len(task.plan.steps), "completed": task.plan.completed})
            return response_text
        action = self.action_router.route(interpretation, request_id=request.request_id)
        if action.handled:
            if action.ok:
                response_text = action.message
            else:
                response_text = action.message
            self.conversation.add("assistant", response_text)
            self.conversation_state.add("assistant", response_text)
            self.events.publish("intelligence.interpreted", interpretation.as_dict())
            self.events.publish("action.routed", {
                "target": action.target,
                "kind": action.kind,
                "ok": action.ok,
                "request_id": request.request_id,
            })
            return response_text
        decision = self.decision_engine.decide(self.context_builder.as_prompt(built) + "\nRelevant task memory: " + str(memory_context) + "\nRelevant conversation memory:\n" + conversation_context)
        composed = self.response_composer.compose(decision)
        self.conversation.add("assistant", composed.text)
        self.conversation_state.add("assistant", composed.text)
        self.conversation_memory.remember(self.context.session_id, "assistant", composed.text)
        self.events.publish("intelligence.interpreted", interpretation.as_dict())
        self.events.publish("intelligence.response.composed", {
            "provider": composed.provider,
            "confidence": composed.confidence,
            "requires_review": composed.requires_review,
            "intent": interpretation.intent,
            "target": interpretation.target,
        })
        return composed.text

    def _command_memory(self, request: CommandRequest) -> str:
        parts = request.text.split(maxsplit=1)
        query = parts[1] if len(parts) > 1 else ""
        return str(self.task_memory.summary(query))
    def _command_run(self, request: CommandRequest) -> str:
        parts = request.text.split(maxsplit=1)
        goal = parts[1] if len(parts) > 1 else ""
        result = self.task_executor.execute(goal, task_id=request.request_id or None)
        if result.ok:
            values = [item.message for item in result.results]
            return str({"task_id": result.task_id, "status": "completed", "results": values})
        return str({"task_id": result.task_id, "status": "failed", "error": result.error, "results": [item.message for item in result.results]})
    def _command_plan(self, request: CommandRequest) -> str:
        parts = request.text.split(maxsplit=1)
        goal = parts[1] if len(parts) > 1 else ""
        plan = self.planning.create_plan(goal)
        return str({"goal": plan.goal, "steps": [step.description for step in plan.steps]})

    def _command_exit(self, request: CommandRequest) -> str:
        self.stop()
        return "WEBSTER stopped."
