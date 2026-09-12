from app.services.quality_scorer import calculate_score


def test_perfect_score():
    assert calculate_score([]) == 100


def test_warning_penalty():
    issues = [
        {
            "severity": "warning",
        }
    ]

    assert calculate_score(issues) == 90


def test_error_penalty():
    issues = [
        {
            "severity": "error",
        }
    ]

    assert calculate_score(issues) == 80


def test_score_never_goes_below_zero():
    issues = [
        {
            "severity": "error",
        }
    ] * 10

    assert calculate_score(issues) == 0