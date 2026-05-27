import json
from openai import OpenAI, OpenAIError


client = OpenAI()


def analyze_resume_with_ai(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are an expert technical recruiter and ATS resume reviewer.

Analyze how well the resume matches the job description below.

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

Job description:
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
                    "content": "You review developer resumes and return strict JSON only.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        raw_content = response.choices[0].message.content
        data = json.loads(raw_content)

        return {
            "ats_score": int(data.get("ats_score", 0)),
            "keyword_match_score": int(data.get("keyword_match_score", 0)),
            "summary": data.get("summary", ""),
            "strengths": data.get("strengths", []),
            "weaknesses": data.get("weaknesses", []),
            "missing_keywords": data.get("missing_keywords", []),
            "ats_observations": data.get("ats_observations", []),
            "suggestions": data.get("suggestions", []),
        }

    except (OpenAIError, json.JSONDecodeError, TypeError, ValueError) as error:
        current_app_error = str(error)

        return {
            "ats_score": 0,
            "keyword_match_score": 0,
            "summary": "Resume analysis could not be completed right now.",
            "strengths": [],
            "weaknesses": [],
            "missing_keywords": [],
            "ats_observations": [],
            "suggestions": [
                "Try running the analysis again.",
                "Check whether the resume text was extracted correctly.",
                "If the issue continues, verify your OpenAI API key and quota.",
            ],
            "error": current_app_error,
        }