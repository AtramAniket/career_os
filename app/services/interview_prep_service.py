import json

from openai import OpenAI

from app.helpers import build_interview_prep_prompt


client = OpenAI(timeout=25)


def generate_interview_prep(application, resume_text, resume_analysis=None):
    prompt = build_interview_prep_prompt(
        application=application,
        resume_text=resume_text,
        resume_analysis=resume_analysis,
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You generate structured interview preparation as valid JSON only.",
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