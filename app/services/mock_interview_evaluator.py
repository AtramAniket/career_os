from __future__ import annotations

import json
from openai import OpenAI

client = OpenAI()


def evaluate_mock_answer(*, question: str, answer: str, role_title: str, company_name: str | None = None) -> dict:
    prompt = f"""
You are an interview coach evaluating a mock interview answer.

Role: {role_title}
Company: {company_name or "Not specified"}

Question:
{question}

Candidate Answer:
{answer}

Return JSON only with:
{{
  "ai_score": number from 1 to 10,
  "ai_feedback": "specific helpful feedback",
  "ai_improved_answer": "a stronger sample answer"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You evaluate mock interview answers and return valid JSON only.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.4,
    )

    content = response.choices[0].message.content
    return json.loads(content)