from app.services.analyzer import analyze_code


def test_detects_division():
    code = """
def divide(a, b):
    return a / b
"""

    issues = analyze_code(code)

    assert len(issues) == 1
    assert issues[0].rule == "DIVISION"
    assert issues[0].severity == "warning"


def test_valid_code_has_no_issues():
    code = """
def add(a, b):
    return a + b
"""

    issues = analyze_code(code)

    assert issues == []


def test_detects_syntax_error():
    code = """
def broken(
"""

    issues = analyze_code(code)

    assert len(issues) == 1
    assert issues[0].rule == "SYNTAX_ERROR"
    assert issues[0].severity == "error"
    