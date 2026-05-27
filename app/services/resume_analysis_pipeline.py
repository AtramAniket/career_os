import os

from flask import current_app

from app.extensions import db
from app.helpers import extract_text_from_pdf
from app.models import ApplicationDocument, ResumeAnalysis
from app.services.resume_analysis_service import analyze_resume_with_ai



def run_resume_analysis(application):
    primary_resume = (
        ApplicationDocument.query
        .filter_by(
            is_primary=True,
            document_type="resume",
            job_application_id=application.id,
        )
        .first()
    )

    if not application.job_description:
        return False, "Add a job description before running analysis."

    if not primary_resume:
        return False, "Please set a primary resume before running analysis."

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    file_path = os.path.join(upload_folder, primary_resume.stored_filename)

    if not os.path.exists(file_path):
        return False, "Resume file is missing from storage."

    resume_text = extract_text_from_pdf(file_path)

    if not resume_text:
        return False, "Unable to extract text from resume."

    ai_result = analyze_resume_with_ai(
        resume_text=resume_text,
        job_description=application.job_description,
    )

    ResumeAnalysis.query.filter_by(
        analysis_type="resume_review",
        document_id=primary_resume.id,
        job_application_id=application.id,
    ).update(
        {"is_latest": False},
        synchronize_session=False
    )

    analysis = ResumeAnalysis(
        is_latest=True,      
        analysis_type="resume_review",
        document_id=primary_resume.id,
        job_application_id=application.id,
        ats_score=ai_result.get("ats_score"),  
        strengths=ai_result.get("strengths", []),
        weakness=ai_result.get("weaknesses", []),
        analysis_summary=ai_result.get("summary"),
        suggestions=ai_result.get("suggestions", []),
        missing_keywords=ai_result.get("missing_keywords", []),
        ats_observations=ai_result.get("ats_observations", []),
        keyword_match_score=ai_result.get("keyword_match_score"),
    )

    db.session.add(analysis)
    db.session.commit()

    return True, "Resume analysis completed."