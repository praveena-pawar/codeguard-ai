from fastapi import APIRouter

from app.schemas.analysis import AnalysisRequest
from app.services.ai_service import explain_issue
from app.services.analyzer import analyze_code

router = APIRouter()


@router.post("/analysis")
def analyze(request: AnalysisRequest):
    issues = analyze_code(request.code)

    results = []

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

    return {
        "issues": results
    }