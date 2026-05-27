import os

from flask import current_app

from app.extensions import db
from app.helpers import extract_text_from_pdf
from app.models import ApplicationDocument, ResumeAnalysis
from app.services import generate_tailoring_suggestions


def run_resume_tailoring(application):

    primary_resume = (
        ApplicationDocument.query
        .filter_by(
            job_application_id=application.id,
            document_type="resume",
            is_primary=True,
        )
        .first()
    )

    if not primary_resume:
        return False, "Please set a primary resume first."

    if not application.job_description:
        return False, "Please add a job description first."

    file_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        primary_resume.stored_filename,
    )

    if not os.path.exists(file_path):
        return False, "Resume file is missing."

    resume_text = extract_text_from_pdf(file_path)

    if not resume_text:
        return False, "Unable to extract resume text."

    ai_result = generate_tailoring_suggestions(
        resume_text=resume_text,
        job_description=application.job_description,
    )

    ResumeAnalysis.query.filter_by(
        job_application_id=application.id,
        document_id=primary_resume.id,
        analysis_type="tailoring",
    ).update(
        {"is_latest": False},
        synchronize_session=False,
    )

    analysis = ResumeAnalysis(
        job_application_id=application.id,
        document_id=primary_resume.id,
        analysis_type="tailoring",
        is_latest=True,
        improved_summary=ai_result.get("improved_summary"),
        missing_keywords=ai_result.get("missing_keywords", []),
        bullet_improvements=ai_result.get("bullet_improvements", []),
        suggestions=ai_result.get("ats_improvements", []),
        analysis_summary=ai_result.get("recruiter_impression"),
    )

    db.session.add(analysis)
    db.session.commit()

    return True, "Tailoring suggestions generated successfully."