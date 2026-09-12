from groq import Groq

from app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def generate_fix(code: str, issue: dict) -> str:
    prompt = f"""
You are an expert Python software engineer.

Fix the following issue in the provided Python code.

CODE:
{code}

ISSUE:
Rule: {issue["rule"]}
Message: {issue["message"]}
Line: {issue["line"]}
Severity: {issue["severity"]}

Requirements:
1. Fix the identified issue.
2. Preserve the original behavior wherever possible.
3. Preserve existing exception types and function behavior unless the issue explicitly requires changing them.
4. The generated fix must remain compatible with expected existing behavior.
5. Return ONLY the complete fixed Python code.
6. Do not include markdown fences.
7. Do not include explanations.
8. Make sure the returned code is valid Python.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content