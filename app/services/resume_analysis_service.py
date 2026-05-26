import json
from openai import OpenAI


client = OpenAI()


def analyze_resume_with_ai(resume_text: str) -> dict:
    """
    Send extracted resume text to OpenAI and return structured resume analysis.
    """

    prompt = f"""
You are an expert technical recruiter and ATS resume reviewer.

Analyze the resume below for a Python/Flask/full-stack developer role.

Return ONLY valid JSON in this exact structure:

{{
  "ats_score": 0,
  "keyword_match_score": 0,
  "summary": "",
  "strengths": [],
  "weaknesses": [],
  "missing_keywords": [],
  "ats_observations": [],
  "suggestions": []
}}

Rules:
- Keep feedback practical and specific.
- Do not invent experience.
- Mention missing skills only if relevant.
- Use simple language.
- Each list item should be short but useful.
- ats_score and keyword_match_score should be integers between 0 and 100.

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You review developer resumes and return strict JSON only.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
    )

    raw_content = response.choices[0].message.content

    try:
        return json.loads(raw_content)
    except json.JSONDecodeError:
        return {
            "ats_score": 0,
            "keyword_match_score": 0,
            "summary": "AI analysis could not be parsed correctly.",
            "strengths": [],
            "weaknesses": [],
            "missing_keywords": [],
            "ats_observations": [],
            "suggestions": [
                "Try running the analysis again.",
                "Check whether the resume text was extracted correctly.",
            ],
        }