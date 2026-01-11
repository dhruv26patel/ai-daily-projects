from src.schema import SummaryResult


def test_schema_valid_example():
    """
    This test makes sure our schema works.
    It's not calling the AI (tests should be fast + stable).
    """
    obj = SummaryResult(
        summary="Service started, some warnings and a retryable error occurred.",
        top_issues=["Redis slow connection", "Payment API 502", "Disk usage high"],
        action_items=["Investigate Redis latency", "Check Payment API health", "Clean disk space"],
        severity="medium",
    )
    assert obj.severity in ["low", "medium", "high"]
    assert len(obj.top_issues) >= 1
    assert len(obj.action_items) >= 1
