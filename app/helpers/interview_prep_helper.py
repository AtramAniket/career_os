def build_interview_prep_prompt(application, resume_text, resume_analysis=None):
    return f"""
You are an experienced technical recruiter and interview preparation assistant.

Generate interview preparation for this specific job application.

Role:
{application.role_title}

Company:
{application.company_name}

Job Description:
{application.job_description or "No job description provided."}

Resume Text:
{resume_text}

Resume Analysis:
{resume_analysis or "No resume analysis provided."}

Important:
- Questions must be based on the job description and resume match.
- Avoid generic questions.
- Generate enough questions to be reused later in mock interview sessions.
- Focus on what a recruiter or hiring manager is likely trying to verify.
- Include questions that test fit, technical ability, projects, resume claims, and possible gaps.

Return valid JSON only with this structure:

{{
  "strategy_summary": "...",

  "hr_questions": [
    {{
      "question": "...",
      "why_it_might_be_asked": "...",
      "answer_guidance": "..."
    }}
  ],

  "technical_questions": [
    {{
      "question": "...",
      "why_it_might_be_asked": "...",
      "answer_guidance": "..."
    }}
  ],

  "project_questions": [
    {{
      "question": "...",
      "why_it_might_be_asked": "...",
      "answer_guidance": "..."
    }}
  ],

  "resume_based_questions": [
    {{
      "question": "...",
      "why_it_might_be_asked": "...",
      "answer_guidance": "..."
    }}
  ],

  "red_flags_to_prepare_for": [
    {{
      "question": "...",
      "why_it_might_be_asked": "...",
      "answer_guidance": "..."
    }}
  ]
}}

Question count:
- hr_questions: 3 questions
- technical_questions: 5 questions
- project_questions: 5 questions
- resume_based_questions: 5 questions
- red_flags_to_prepare_for: 2 questions

Total: 20 questions.
"""