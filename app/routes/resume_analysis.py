import os

from flask_login import login_required, current_user
from flask import Blueprint, url_for, render_template, redirect, abort, flash, current_app

from app.extensions import db
from app.helpers import allowed_document_file, extract_text_from_pdf
from app.models import ApplicationDocument, JobApplication, ResumeAnalysis
from app.services import run_resume_analysis, run_resume_tailoring

resume_analysis_bp = Blueprint("resume_analysis", __name__, url_prefix='/applications')


@resume_analysis_bp.route("/<int:application_id>/tailor_resume", methods=["POST"])
@login_required
def analyze(application_id):

	application = JobApplication.query.get_or_404(application_id)

	if application.user_id != current_user.id:
		abort(404)

	success, message = run_resume_tailoring(application)


	flash(message, "success" if success else "warning")

	return redirect(url_for("applications.detail", application_id=application.id))



@resume_analysis_bp.route("/<int:application_id>/resume_analysis", methods=["POST"])
@login_required
def tailor_resume(application_id):

	application = JobApplication.query.get_or_404(application_id)

	if application.user_id != current_user.id:
		abort(404)

	success, message = run_resume_analysis(application)


	flash(message, "success" if success else "warning")

	return redirect(url_for("applications.detail", application_id=application.id))