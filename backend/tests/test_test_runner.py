from app.services.test_runner import run_tests


def test_run_tests_passes():
    source_code = """
def add(a, b):
    return a + b
"""


    test_code = """
def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5
"""

    result = run_tests(source_code, test_code)

    assert result["passed"] is True
    assert result["return_code"] == 0
    assert "1 passed" in result["stdout"]