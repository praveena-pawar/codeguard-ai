from groq import Groq

from app.core.config import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)


def generate_tests(code: str, issues: list[dict]) -> str:
    prompt = f"""
You are an expert Python testing engineer.

Generate pytest tests for the following Python code.

SOURCE CODE:
{code}

DETECTED ISSUES:
{issues}

IMPORTANT:
- The source code will be saved as solution.py.
- The tests will be saved as test_solution.py.
- Import functions/classes from solution.
- Do NOT redefine source functions/classes.
- Tests must verify CORRECT expected behavior.
- NEVER write tests that expect buggy behavior.
- Tests must pass against the corrected implementation.
- Tests must fail against the original buggy implementation when testing the
  detected bug.

Requirements:
1. Use pytest.
2. Test behavior that is directly supported by the source code and detected issue.
3. Test normal/expected behavior.
4. Test important edge cases related to the detected issue.
5. Do not invent new business requirements or change the intended API behavior.
6. Do not assert that a previously returned mutable object remains unchanged after
   the same object is intentionally mutated later.
7. For a DIVISION issue, test division by zero using:
       with pytest.raises(ValueError):
           function_name(..., 0)
8. For a MUTABLE_DEFAULT issue, verify that separate calls using the default
   argument receive independent list/dict/set objects.
9. For a KEY_ERROR issue, test safe handling of a missing dictionary key.
10. For subprocess/security issues, do not assume a specific exception type
    unless the source code or issue clearly requires it.
11. Return ONLY valid Python test code.
12. Do not include markdown fences.
13. Do not include explanations.


DIVISION ISSUE:

If the issue rule is DIVISION:

- Test normal division.
- Test division by zero.
- The corrected behavior must raise ValueError.

Example:

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)


KEY_ERROR ISSUE:

If the issue rule is KEY_ERROR:

The original implementation may directly access a dictionary key:

    return users[user_id]

This can raise KeyError when the key does not exist.

Generate a test that verifies the corrected implementation handles a missing
key safely.

The preferred corrected behavior is:

    return users.get(user_id)

Therefore, when testing a missing key:

- Do NOT expect KeyError.
- Do NOT expect ValueError.
- Do NOT use pytest.raises().
- Call the function with a missing key.
- Assert that the result is None.

Example:

def test_get_user_missing_key_returns_none():
    users = dict(
        [(1, dict(name="Alice"))]
    )

    result = get_user(users, 999)

    assert result is None


For an existing key, verify that the correct value is returned.

Example:

def test_get_user_existing_key():
    users = dict(
        [(1, dict(name="Alice"))]
    )

    result = get_user(users, 1)

    assert result == dict(name="Alice")


MUTABLE_DEFAULT ISSUE:

If the issue rule is MUTABLE_DEFAULT or B006:

The problem is that a mutable default object such as [] is shared between
different function calls.

Test ONLY that separate calls using the DEFAULT argument receive independent
objects.

For example, if the function is:

    def add_item(item, items=[]):
        items.append(item)
        return items

generate a test equivalent to:

def test_add_item_default_is_independent():
    first = add_item("a")
    second = add_item("b")
    third = add_item("c")

    assert first == ["a"]
    assert second == ["b"]
    assert third == ["c"]

    assert first is not second
    assert second is not third
    assert first is not third

    assert "a" not in second
    assert "a" not in third
    assert "b" not in third


CRITICAL MUTABLE_DEFAULT RULES:

- Do NOT test explicit list arguments.
- Do NOT test accumulation using an externally supplied list.
- Do NOT compare a list AFTER it has been mutated by a later call.
- Do NOT expect shared state.
- Do NOT assert that a second default call contains the first call's item.
- Do NOT write tests demonstrating the buggy behavior as the expected result.
- Focus exclusively on independent default objects.

The corrected implementation should behave like:

    def add_item(item, items=None):
        if items is None:
            items = []

        items.append(item)
        return items

The generated test must PASS for that corrected implementation.

The generated test must FAIL for:

    def add_item(item, items=[]):
        items.append(item)
        return items


GENERAL RULE:

Always generate tests that represent the intended CORRECT behavior.

The tests should expose the detected bug in the original implementation
and pass after the AI-generated correction.

Return only the pytest code.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content