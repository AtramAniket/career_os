import json
from openai import OpenAI, OpenAIError


client = OpenAI()


def generate_tailoring_suggestions(
    resume_text: str,
    job_description: str,
) -> dict:

    prompt = f"""
You are an expert technical recruiter helping tailor a resume for a software engineering role.

Analyze the resume against the job description.

Return ONLY valid JSON in this exact structure:

{{
  "improved_summary": "",
  "missing_keywords": [],
  "bullet_improvements": [],
  "ats_improvements": [],
  "recruiter_impression": ""
}}

Rules:
- Keep suggestions realistic.
- Do not invent fake experience.
- Suggestions should improve ATS compatibility.
- Bullet improvements should be concise.
- Use simple and professional language.

Resume:
\"\"\"
{resume_text}
\"\"\"

Job Description:
\"\"\"
{job_description}
\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You help improve resumes and return strict JSON only.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.4,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        return {
            "improved_summary": data.get("improved_summary", ""),
            "missing_keywords": data.get("missing_keywords", []),
            "bullet_improvements": data.get("bullet_improvements", []),
            "ats_improvements": data.get("ats_improvements", []),
            "recruiter_impression": data.get("recruiter_impression", ""),
        }

    except (OpenAIError, json.JSONDecodeError, TypeError, ValueError):
        return {
            "improved_summary": "",
            "missing_keywords": [],
            "bullet_improvements": [],
            "ats_improvements": [],
            "recruiter_impression": "Unable to generate tailoring suggestions right now.",
        }