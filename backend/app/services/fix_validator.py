from app.services.test_runner import run_tests


def validate_fix(fixed_code: str, test_code: str) -> dict:
    return run_tests(
        source_code=fixed_code,
        test_code=test_code,
    )