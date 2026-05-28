def build_interview_prep_prompt(application, resume_text, resume_analysis=None):
    return f"""
You are an interview preparation assistant.

Generate interview prep for this job application.

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

Return structured JSON with:
- strategy_summary
- hr_questions
- technical_questions
- project_questions
- resume_based_questions
- red_flags_to_prepare_for

Each question should include:
- question
- why_it_might_be_asked
- answer_guidance
"""