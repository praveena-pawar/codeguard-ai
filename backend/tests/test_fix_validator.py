from app.services.fix_validator import validate_fix


def test_validate_fix_passes():
    fixed_code = """
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
"""

    test_code = """
import pytest


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
"""

    result = validate_fix(
        fixed_code=fixed_code,
        test_code=test_code,
    )

    assert result["passed"] is True
    assert result["return_code"] == 0