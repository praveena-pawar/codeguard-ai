from fastapi import APIRouter
from app.services.database import create_project, create_analysis, create_issue, create_test_run, create_fix

from app.schemas.analysis import AnalysisRequest
from app.services.ai_fix_service import generate_fix
from app.services.ai_service import explain_issue
from app.services.analyzer import analyze_code
from app.services.quality_scorer import calculate_score
from app.services.test_generator import generate_tests
from app.services.test_runner import run_tests
from app.services.fix_validator import validate_fix


router = APIRouter()



@router.post("/analysis")
def analyze(request: AnalysisRequest):
    # 1. Analyze the submitted code
    issues = analyze_code(request.code)

    results = []

    # 2. Explain every detected issue
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

    # 3. Generate tests based on the detected issues
    test_code = generate_tests(
        request.code,
        results,
    )

    # 4. Run generated tests against the original code
    original_test_result = run_tests(
        source_code=request.code,
        test_code=test_code,
    )

    # 5. Calculate the BEFORE quality score
    before_score = calculate_score(
        issues,
        tests_passed=original_test_result["passed"],
    )

    # 6. Default values
    fixed_code = request.code
    fixed_test_result = original_test_result

    # 7. Generate a fix if issues were found
    if issues:
        first_issue = results[0]

        fixed_code = generate_fix(
            request.code,
            first_issue,
        )

        # 8. Validate the generated fix
        fixed_test_result = validate_fix(
            fixed_code=fixed_code,
            test_code=test_code,
        )

    # 9. Re-analyze the fixed code
    fixed_issues = analyze_code(fixed_code)

    # 10. Calculate the AFTER quality score
    after_score = calculate_score(
        fixed_issues,
        tests_passed=fixed_test_result["passed"],
        fix_validated=fixed_test_result["passed"],
    )

    project = create_project("CodeGuard Demo")

    analysis = create_analysis(
        project_id=project["id"],
        code=request.code,
        before_score=before_score,
        after_score=after_score,
    )


    for issue in results:
        create_issue(
            analysis_id=analysis["id"],
            rule=issue["rule"],
            message=issue["message"],
            line=issue["line"],
            severity=issue["severity"],
            explanation=issue["explanation"],
        )


    create_test_run(
        analysis_id=analysis["id"],
        test_code=test_code,
        original_passed=original_test_result["passed"],
        original_output=(
            original_test_result["stdout"]
            + original_test_result["stderr"]
        ),
        fixed_passed=fixed_test_result["passed"],
        fixed_output=(
            fixed_test_result["stdout"]
            + fixed_test_result["stderr"]
        ),
    )

    create_fix(
        analysis_id=analysis["id"],
        fixed_code=fixed_code,
        validated=fixed_test_result["passed"],
    )




    # 11. Return the complete analysis result
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


