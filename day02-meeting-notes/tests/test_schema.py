from src.schema import SummaryResult, ActionItem


def test_project2_schema_valid_example():
    """
    Unit test for Project 2 schema.
    This test does NOT call the AI.
    It only verifies schema validation works correctly.
    """

    obj = SummaryResult(
        summary="Discussed backend issues and assigned follow-up tasks.",
        action_items=[
            ActionItem(
                task="Investigate Redis latency",
                owner="John",
                priority="high",
                due_date="Friday",
            ),
            ActionItem(
                task="Check payment gateway failures",
                owner="Priya",
                priority="medium",
                due_date="unknown",
            ),
            ActionItem(
                task="Reduce disk usage on prod servers",
                owner="unassigned",
                priority="medium",
                due_date="unknown",
            ),
        ],
    )

    # Basic assertions
    assert isinstance(obj.summary, str)
    assert len(obj.action_items) >= 1

    # Check each action item
    for item in obj.action_items:
        assert item.task != ""
        assert item.owner != ""
        assert item.priority in ["low", "medium", "high"]
        assert isinstance(item.due_date, str)
