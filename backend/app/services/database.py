from app.core.supabase import supabase


def create_project(name: str) -> dict:
    response = (
        supabase
        .table("projects")
        .insert({"name": name})
        .execute()
    )

    return response.data[0]


def create_analysis(
    project_id: str,
    code: str,
    before_score: int,
    after_score: int,
) -> dict:
    response = (
        supabase
        .table("analyses")
        .insert(
            {
                "project_id": project_id,
                "code": code,
                "before_score": before_score,
                "after_score": after_score,
            }
        )
        .execute()
    )

    return response.data[0]




def create_issue(
    analysis_id: str,
    rule: str,
    message: str,
    line: int,
    severity: str,
    explanation: str,
) -> dict:
    response = (
        supabase
        .table("issues")
        .insert(
            {
                "analysis_id": analysis_id,
                "rule": rule,
                "message": message,
                "line": line,
                "severity": severity,
                "explanation": explanation,
            }
        )
        .execute()
    )

    return response.data[0]



def create_test_run(
    analysis_id: str,
    test_code: str,
    original_passed: bool,
    original_output: str,
    fixed_passed: bool,
    fixed_output: str,
) -> dict:
    response = (
        supabase
        .table("test_runs")
        .insert(
            {
                "analysis_id": analysis_id,
                "test_code": test_code,
                "original_passed": original_passed,
                "original_output": original_output,
                "fixed_passed": fixed_passed,
                "fixed_output": fixed_output,
            }
        )
        .execute()
    )
    return response.data[0]



def create_fix(
    analysis_id: str,
    fixed_code: str,
    validated: bool,
) -> dict:
    response = (
        supabase
        .table("fixes")
        .insert(
            {
                "analysis_id": analysis_id,
                "fixed_code": fixed_code,
                "validated": validated,
            }
        )
        .execute()
    )
    return response.data[0]