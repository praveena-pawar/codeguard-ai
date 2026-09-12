import ast

from app.services.ai_fix_service import generate_fix


def test_generate_fix_returns_code():
    code = """
def divide(a, b):
    return a / b
"""

    issue = {
        "rule": "DIVISION",
        "message": "Division operation detected. Make sure the denominator cannot be zero.",
        "line": 3,
        "severity": "warning",
    }

    fixed_code = generate_fix(code, issue)

    assert fixed_code
    assert "def divide" in fixed_code
    assert "return" in fixed_code


def test_generate_fix_returns_valid_python():
    code = """
def divide(a, b):
    return a / b
"""

    issue = {
        "rule": "DIVISION",
        "message": "Division operation detected. Make sure the denominator cannot be zero.",
        "line": 3,
        "severity": "warning",
    }

    fixed_code = generate_fix(code, issue)

    ast.parse(fixed_code)