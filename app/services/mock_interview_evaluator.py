from __future__ import annotations

import json
from typing import Any

from openai import OpenAI

client = OpenAI()


def evaluate_mock_answer(
    *,
    question: str,
    answer: str,
    role_title: str,
    company_name: str | None = None,
) -> dict[str, Any]:
    prompt = f"""
You are an interview coach evaluating a candidate's mock interview answer.

Role: {role_title}
Company: {company_name or "Not specified"}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer fairly and practically.

Return valid JSON only using this exact structure:
{{
  "ai_score": 1,
  "ai_feedback": "Specific feedback on what was good, what was missing, and how to improve.",
  "ai_improved_answer": "A stronger sample answer the candidate could give."
}}

Scoring guide:
1-3 = weak or unclear answer
4-6 = okay but incomplete answer
7-8 = strong answer with some room to improve
9-10 = excellent interview-ready answer
"""

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a concise, practical interview coach. Return JSON only.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.4,
    )

    content = completion.choices[0].message.content

    if not content:
        raise ValueError("Empty AI evaluation response.")

    data = json.loads(content)

    return {
        "ai_score": data.get("ai_score"),
        "ai_feedback": data.get("ai_feedback"),
        "ai_improved_answer": data.get("ai_improved_answer"),
    }


def evaluate_mock_session(
    *,
    role_title: str,
    company_name: str | None,
    qa_pairs: list[dict[str, Any]],
) -> dict[str, Any]:
    prompt = f"""
You are an interview coach evaluating a full mock interview session.

Role: {role_title}
Company: {company_name or "Not specified"}

Evaluate each answer separately.

Questions and answers:
{json.dumps(qa_pairs, indent=2)}

Return valid JSON only using this exact structure:
{{
  "evaluations": [
    {{
      "question_id": 1,
      "ai_score": 1,
      "ai_feedback": "Specific feedback for this answer.",
      "ai_improved_answer": "A stronger sample answer."
    }}
  ]
}}

Rules:
- Use the exact question_id from the input.
- Score each answer from 1 to 10.
- Be practical, concise, and interview-focused.
- Do not skip any answered question.
"""

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a practical interview coach. Return JSON only.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.4,
    )

    content = completion.choices[0].message.content

    if not content:
        raise ValueError("Empty AI evaluation response.")

    return json.loads(content)