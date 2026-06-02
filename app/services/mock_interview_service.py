import json
from openai import OpenAI
from flask import current_app


def generate_mock_interview_questions(application):
    client = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])

    prompt = f"""
You are an experienced technical recruiter and interviewer.

Create 5 mock interview questions for this specific job application.

Company:
{application.company_name}

Role:
{application.role_title}

Job Description:
{application.job_description or "No job description provided."}

Rules:
- Questions must be based on the job description.
- Avoid generic interview questions.
- Focus on what the recruiter is likely trying to verify.
- Include technical, role-fit, project, behavioral, and gap-probe style questions.
- Keep questions clear and interview-like.

Return JSON only in this format:

{{
  "questions": [
    {{
      "category": "technical",
      "question": "..."
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You generate job-specific mock interview questions. Return valid JSON only.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.4,
    )

    raw_content = response.choices[0].message.content

    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError:
        return _fallback_questions(application)

    questions = parsed.get("questions", [])

    if not questions:
        return _fallback_questions(application)

    return questions[:5]


def _fallback_questions(application):
    role = application.role_title or "this role"

    return [
        {
            "category": "role_fit",
            "question": f"What interests you about the {role} position, based on the responsibilities in the job description?",
        },
        {
            "category": "technical",
            "question": f"Which technical requirement from this {role} role best matches your experience, and how have you used it in a real project?",
        },
        {
            "category": "project_experience",
            "question": "Walk me through a project that best proves you can handle the responsibilities mentioned in this job description.",
        },
        {
            "category": "behavioral",
            "question": "Tell me about a time you had to learn something quickly to complete a project or task.",
        },
        {
            "category": "closing",
            "question": f"Why would you be a strong fit for this {role} role?",
        },
    ]