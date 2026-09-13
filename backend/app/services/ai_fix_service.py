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
7. The generated code must satisfy the detected issue and pass the tests
   generated for the corrected behavior.

IMPORTANT RULE-SPECIFIC FIXES:

For DIVISION:
- Explicitly guard against a zero denominator.
- Raise ValueError with a clear message instead of allowing ZeroDivisionError.
- Example:

    def divide(a, b):
        if b == 0:
            raise ValueError("Denominator cannot be zero.")
        return a / b


For KEY_ERROR:
- If the issue is caused by directly accessing a dictionary key such as:

    return users[user_id]

  change the implementation so that a missing key is handled safely.

- For this CodeGuard rule, the preferred corrected behavior is to return None
  when the requested key does not exist.

- Use dictionary.get() for the lookup.

- Example:

    def get_user(users, user_id):
        return users.get(user_id)

- Do NOT raise KeyError for a missing key.
- Do NOT create a custom exception for a missing key.
- Do NOT use:

    raise KeyError(...)

- Do NOT use:

    if user_id in users:
        return users[user_id]
    raise KeyError(...)

- The corrected implementation must allow:

    get_user(users, missing_id)

  to return None.


For MUTABLE_DEFAULT:
- Never use a mutable object such as [], {{}}, or set() as a function default.
- Replace the mutable default with None.
- Initialize the mutable object inside the function when the argument is None.
- Preserve the behavior of explicitly supplied lists/dictionaries/sets.

Example:

    def add_item(item, items=None):
        if items is None:
            items = []
        items.append(item)
        return items


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
- Preserve the behavior of explicitly supplied mutable arguments.


FINAL VALIDATION RULE:

Before returning the code, verify that the corrected implementation actually
satisfies the detected issue.

For KEY_ERROR specifically:

- Existing keys must still return their associated value.
- Missing keys must return None.
- Do not raise KeyError for missing keys.
- The preferred implementation is dictionary.get().

For example:

    users = dict(
        [(1, dict(name="Alice"))]
    )

    get_user(users, 1)
    -> dict(name="Alice")

    get_user(users, 999)
    -> None

Return ONLY the complete corrected Python source code.
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