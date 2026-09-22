from WEBSTER_REFERENCE.intelligence.multi_turn_reasoning import ReasoningContext
from WEBSTER_REFERENCE.intelligence.robust_planner import RobustPlanner


def test_plan_verifies_available_calculator() -> None:
    planner = RobustPlanner()
    plan = planner.build(
        "calculate 12 * 7",
        context=ReasoningContext("session"),
        available_tools=("calculator",),
    )
    assert plan.executable
    assert plan.steps[0].capabilities == ("local.compute",)
    assert plan.confidence > 0.0


def test_plan_blocks_missing_capability() -> None:
    planner = RobustPlanner()
    plan = planner.build(
        "open the browser then calculate 4 + 5",
        context=ReasoningContext("session"),
        available_tools=("calculator",),
    )
    assert not plan.executable
    assert any("browser.execute" in blocker for blocker in plan.blockers)


def test_plan_carries_constraints_and_evidence() -> None:
    planner = RobustPlanner()
    context = ReasoningContext("session")
    context.set_constraints(["under 10 seconds"])
    plan = planner.build("calculate 2 + 3", context=context, available_tools=("calculator",))
    assert plan.constraints == ("under 10 seconds",)
