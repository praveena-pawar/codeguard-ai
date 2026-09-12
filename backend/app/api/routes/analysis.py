from fastapi import APIRouter

from app.schemas.analysis import AnalysisRequest
from app.services.analyzer import analyze_code


router = APIRouter()


@router.post("/analysis")
def analyze(request: AnalysisRequest):
    issues = analyze_code(request.code)

    return {
        "issues": [
            {
                "rule": issue.rule,
                "message": issue.message,
                "line": issue.line,
                "severity": issue.severity,
            }
            for issue in issues
        ]
    }