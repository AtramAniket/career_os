from flask_login import login_required, current_user
from flask import Blueprint, url_for, render_template, redirect, abort, flash

from app.models import ApplicationDocument, JobApplication
from app.extensions import db

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

	if not application.job_descritpion:
		flash("Add a job description before running analysis", "warning")
		return redirect(url_for("applications.detail", application_id=application.id))

	if not primary_resume:
		flash("Please set a primary resume before running analysis", "warning")
		return redirect(url_for("applications.detail", application_id=application.id))

	flash("Resume analysis foundation is ready. AI analysis will be connected later", "info")
	return redirect(url_for("applications.detail", application_id=application.id))

