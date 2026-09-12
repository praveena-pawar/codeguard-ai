def calculate_score(issues: list) -> int:
    score = 100

    penalties = {
        "error": 20,
        "warning": 10,
        "info": 5,
    }

    for issue in issues:
        severity = issue.severity if hasattr(issue, "severity") else issue.get(
            "severity", "info"
        )

        score -= penalties.get(severity, 5)

    return max(score, 0)