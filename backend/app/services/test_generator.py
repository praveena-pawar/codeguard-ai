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
2. Test normal behavior.
3. Test important edge cases.
4. Write at least one test for every detected issue.
5. Return ONLY valid Python test code.
6. Do not include markdown fences.
7. Do not include explanations.

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
- Test an existing key.
- Test a missing key.
- The corrected behavior must raise ValueError.
- Do not use dictionary literals in the generated test unless necessary.

Example:

    def test_missing_user():
        users = dict()
        users[1] = dict(name="Alice")

        with pytest.raises(ValueError):
            get_user(users, 999)

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

Return only the pytest code.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content