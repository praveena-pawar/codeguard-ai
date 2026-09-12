from fastapi import APIRouter

from app.schemas.analysis import AnalysisRequest
from app.services.ai_fix_service import generate_fix
from app.services.ai_service import explain_issue
from app.services.analyzer import analyze_code
from app.services.fix_validator import validate_fix
from app.services.quality_scorer import calculate_score
from app.services.test_generator import generate_tests
from app.services.test_runner import run_tests

router = APIRouter()


@router.post("/analysis")
def analyze(request: AnalysisRequest):
    # 1. Analyze the submitted code
    issues = analyze_code(request.code)

    # 2. Calculate initial quality score
    before_score = calculate_score(issues)

    results = []

    # 3. Explain every detected issue
    for issue in issues:
        issue_data = {
            "rule": issue.rule,
            "message": issue.message,
            "line": issue.line,
            "severity": issue.severity,
        }

        explanation = explain_issue(
            request.code,
            issue_data,
        )

        issue_data["explanation"] = explanation

        results.append(issue_data)

    # 4. Generate tests
    test_code = generate_tests(request.code)

    # 5. Run generated tests against original code
    original_test_result = run_tests(
        source_code=request.code,
        test_code=test_code,
    )

    # 6. Generate a fix if issues were found
    fixed_code = request.code
    fixed_test_result = original_test_result

    if issues:
        first_issue = results[0]

        fixed_code = generate_fix(
            request.code,
            first_issue,
        )

        # 7. Validate the generated fix
        fixed_test_result = validate_fix(
            fixed_code=fixed_code,
            test_code=test_code,
        )

    # 8. Re-analyze the fixed code
    fixed_issues = analyze_code(fixed_code)

    # 9. Calculate final quality score
    after_score = calculate_score(fixed_issues)

    return {
        "issues": results,
        "before_score": before_score,
        "tests": {
            "code": test_code,
            "original": original_test_result,
            "fixed": fixed_test_result,
        },
        "fix": {
            "code": fixed_code,
            "validated": fixed_test_result["passed"],
        },
        "after_score": after_score,
    }