from groq import Groq

from app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def generate_tests(code: str) -> str:
    prompt = f"""
You are an expert Python testing engineer.

Generate pytest tests for the following Python code.

CODE:
{code}

Requirements:
1. Use pytest.
2. Test normal/expected behavior.
3. Test important edge cases.
4. Test likely failure cases.
5. Return ONLY valid Python test code.
6. Do not include markdown fences.
7. Do not include explanations.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content