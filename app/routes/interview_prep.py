from flask_login import login_required, current_user
from flask import abort, redirect, url_for, Blueprint, render_template

from app.models import InterviewPrep, JobApplication

interview_prep_bp = Blueprint(
	"interview_prep",
	__name__,
	url_prefix="/applications/<int:application_id>/interview_prep")


# GET "/applications/1/interview_prep"
@interview_prep_bp.route("/", methods=["GET"])
@login_required
def index(application_id):

	application = JobApplication.query\
	.filter_by(
		id=application_id,
		user_id=current_user.id,
		is_deleted=False)\
	.first_or_404()

	latest_prep = InterviewPrep.query\
	.filter_by(
		job_application_id=application.id,
		is_latest=True)\
	.order_by(InterviewPrep.created_at.desc())\
	.first_or_404()

	prep_history = InterviewPrep.query\
	.filter_by(job_application_id=application.id)\
	.order_by(InterviewPrep.created_at.desc())\
	.all()

	render_template(
		"interview_prep/detail.html",
		application=application,
		latest_prep=latest_prep,
		prep_history=prep_history,
	)