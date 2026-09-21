"""A7 planning and execution tests."""
from WEBSTER_REFERENCE.intelligence.action_router import ActionRouter
from WEBSTER_REFERENCE.intelligence.planning_engine import PlanningEngine
from WEBSTER_REFERENCE.intelligence.progress_reporter import ProgressReporter
from WEBSTER_REFERENCE.intelligence.task_executor import TaskExecutor
from WEBSTER_REFERENCE.tests.test_action_routing_a6 import _tools

def test_multistep_execution_respects_dependencies() -> None:
    executor = TaskExecutor(PlanningEngine(), ActionRouter(tool_dispatcher=_tools()), ProgressReporter())
    result = executor.execute("calculate 2 + 3 then calculate 4 * 5")
    assert result.ok
    assert result.plan.completed == 2
    assert [item.message for item in result.results] == ["5", "20"]

def test_failed_step_stops_following_steps() -> None:
    executor = TaskExecutor(PlanningEngine(), ActionRouter(tool_dispatcher=_tools()), ProgressReporter())
    result = executor.execute("calculate 2 + 3 then unsupported thing")
    assert not result.ok
    assert result.plan.steps[0].status == "completed"
    assert result.plan.steps[1].status == "failed"
