from groq import Groq

from app.core.config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)


def generate_fix(code: str, issue: dict) -> str:
    prompt = f"""
You are an expert Python software engineer.

Fix the identified issue in the provided Python code.

CODE:
{code}

ISSUE:
Rule: {issue["rule"]}
Message: {issue["message"]}
Line: {issue["line"]}
Severity: {issue["severity"]}

Requirements:

1. Fix the identified issue correctly.
2. Preserve the original behavior wherever possible.
3. Return the COMPLETE corrected Python source code.
4. Do not include markdown fences.
5. Do not include explanations.
6. Make sure the returned code is valid Python.

IMPORTANT RULE-SPECIFIC FIXES:

For DIVISION:
- Explicitly guard against a zero denominator.
- Raise ValueError with a clear message instead of allowing ZeroDivisionError.

For MUTABLE_DEFAULT:
- Never use a mutable object such as [], {{}}, or set() as a function default.
- Replace the mutable default with None.
- Initialize the mutable object inside the function when the argument is None.
- Preserve the behavior of explicitly supplied lists/dictionaries/sets.

For PLW1510:
- If subprocess.run() is missing the explicit check argument, add:
    check=True
- Do NOT use check=False as the fix.
- The purpose of this rule is to make subprocess failures raise
  subprocess.CalledProcessError.
- Preserve existing arguments such as shell, capture_output, and text.

For B006:
- Replace mutable default arguments with None.
- Initialize the mutable value inside the function.

The generated code must actually satisfy the detected rule.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content