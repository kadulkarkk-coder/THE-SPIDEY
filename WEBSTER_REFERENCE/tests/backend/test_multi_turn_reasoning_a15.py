from WEBSTER_REFERENCE.intelligence.multi_turn_reasoning import MultiTurnReasoning


def test_long_context_retains_goal_entities_constraints_and_results() -> None:
    manager = MultiTurnReasoning()
    sid = "session-a"
    manager.observe(sid, role="user", text="Help me plan a science project",
                    goal="science project", entities={"topic": "water filtration"},
                    constraints=["under 500 rupees"], intent="planning")
    manager.observe(sid, role="assistant", text="I found three possible approaches",
                    results=["sand filter", "charcoal filter", "ceramic filter"])
    ctx = manager.context(sid)
    assert ctx.goal == "science project"
    assert ctx.resolve("the goal") == "science project"
    assert ctx.resolve("topic") == "water filtration"
    assert "under 500 rupees" in ctx.constraints
    assert ctx.resolve("the last result") == "ceramic filter"


def test_sessions_never_mix() -> None:
    manager = MultiTurnReasoning()
    manager.observe("a", role="user", text="Project A", goal="Project A", entities={"topic": "physics"})
    manager.observe("b", role="user", text="Project B", goal="Project B", entities={"topic": "history"})
    assert manager.context("a").resolve("topic") == "physics"
    assert manager.context("b").resolve("topic") == "history"
    assert manager.context("a").goal != manager.context("b").goal


def test_prompt_is_bounded() -> None:
    manager = MultiTurnReasoning()
    for i in range(50):
        manager.observe("a", role="user", text=f"turn {i} " + "x" * 500)
    assert len(manager.prompt_context("a")) <= 2600
