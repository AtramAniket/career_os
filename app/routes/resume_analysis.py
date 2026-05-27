import os

from flask_login import login_required, current_user
from flask import Blueprint, url_for, render_template, redirect, abort, flash, current_app

from app.extensions import db
from app.services import analyze_resume_with_ai
from app.helpers import allowed_document_file, extract_text_from_pdf
from app.models import ApplicationDocument, JobApplication, ResumeAnalysis

resume_analysis_bp = Blueprint("resume_analysis", __name__, url_prefix='/applications')


@resume_analysis_bp.route("/<int:application_id>/resume_analysis", methods=["POST"])
@login_required
def analyze(application_id):

	application = JobApplication.query.get_or_404(application_id)

	if application.user_id != current_user.id:
		abort(404)

	primary_resume = ApplicationDocument.query\
	.filter_by(
		job_application_id=application.id,
		document_type="resume",
		is_primary=True
		)\
	.first()

	upload_folder = current_app.config["UPLOAD_FOLDER"]
	os.makedirs(upload_folder, exist_ok=True)

	if not primary_resume:
	    flash("There is no resume to analyze. Please add primary resume for analysis", "danger")
	    return redirect(url_for("applications.detail", application_id=application.id))

	file_path = os.path.join(upload_folder, primary_resume.stored_filename)

	resume_text = extract_text_from_pdf(file_path)

	if not resume_text:
	    flash("Unable to extract text from resume.", "danger")
	    return redirect(url_for("applications.detail", application_id=application.id))

	if not application.job_description:
		flash("Add a job description before running analysis", "warning")
		return redirect(url_for("applications.detail", application_id=application.id))

	if not primary_resume:
		flash("Please set a primary resume before running analysis", "warning")
		return redirect(url_for("applications.detail", application_id=application.id))

	ai_result = analyze_resume_with_ai(
		resume_text=resume_text,
		job_description=application.job_description
	)

	ResumeAnalysis.query.filter_by(
	    job_application_id=application.id,
	    document_id=primary_resume.id,
	).delete(synchronize_session=False)

	analysis = ResumeAnalysis(
	    job_application_id=application.id,
	    document_id=primary_resume.id,
	    ats_score=ai_result.get("ats_score"),
	    keyword_match_score=ai_result.get("keyword_match_score"),
	    analysis_summary=ai_result.get("summary"),
	    strengths=ai_result.get("strengths", []),
	    missing_keywords=ai_result.get("missing_keywords", []),
	    suggestions=ai_result.get("suggestions", []),
	    weakness=ai_result.get("weaknesses", []),
	    ats_observations=ai_result.get("ats_observations", []),
	)

	db.session.add(analysis)
	db.session.commit()

	flash("Resume analysis completed.", "success")
	return redirect(url_for("applications.detail", application_id=application.id))

