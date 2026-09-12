from groq import Groq

from app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def explain_issue(code: str, issue: dict) -> str:
    prompt = f"""
You are an expert Python code reviewer.

Analyze the following code issue and explain it to a developer.

CODE:
{code}

ISSUE:
Rule: {issue["rule"]}
Message: {issue["message"]}
Line: {issue["line"]}
Severity: {issue["severity"]}

Explain:
1. What is the problem?
2. Why is it a problem?
3. What could happen because of it?
4. How should the developer fix it?

Keep the explanation concise, practical, and easy to understand.
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