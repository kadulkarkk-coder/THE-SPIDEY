"""A13 persistent entity context tests."""
from WEBSTER_REFERENCE.intelligence.entity_context import EntityContext

def test_reference_survives_multiple_turns() -> None:
    ctx = EntityContext(ttl_seconds=900)
    ctx.observe("calculate 12 * 7")
    assert ctx.resolve("it").value == "12"
    ctx.observe("multiply it by 3")
    ctx.set("last_number", "252")
    assert ctx.resolve("that").value == "252"
    ctx.observe("add that by 50")
    assert ctx.resolve("the result").value == "252"

def test_unknown_reference_does_not_guess() -> None:
    ctx = EntityContext()
    assert ctx.resolve("that").value if ctx.resolve("that") else None is None

def test_explicit_invalidation() -> None:
    ctx = EntityContext()
    ctx.set("last_number", "84")
    assert ctx.resolve("it").value == "84"
    ctx.invalidate("last_number")
    assert ctx.resolve("it") is None


def test_ordered_results_support_natural_references() -> None:
    ctx = EntityContext()
    ctx.set_results(["first-file.txt", "second-file.txt", "third-file.txt"])
    assert ctx.resolve("the first result").value == "first-file.txt"
    assert ctx.resolve("the second result").value == "second-file.txt"
