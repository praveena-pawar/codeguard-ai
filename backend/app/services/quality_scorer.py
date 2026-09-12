def calculate_score(
    issues: list,
    tests_passed: bool | None = None,
    fix_validated: bool | None = None,
) -> int:
    """
    Calculate a code quality score from 0 to 100.

    Static-analysis issues reduce the score based on severity.
    Failed tests and failed fix validation add additional penalties
    when those results are available.
    """

    score = 100

    penalties = {
        "error": 20,
        "warning": 10,
        "info": 5,
    }

    # Static-analysis penalties
    for issue in issues:
        severity = (
            issue.severity
            if hasattr(issue, "severity")
            else issue.get("severity", "info")
        )

        score -= penalties.get(severity, 5)

    # Test validation penalty
    if tests_passed is False:
        score -= 5

    # AI fix validation penalty
    if fix_validated is False:
        score -= 10

    return max(0, min(score, 100))