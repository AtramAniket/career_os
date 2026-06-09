from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models import JobApplication

ai_insights_bp = Blueprint("ai_insights", __name__, url_prefix="/ai_insights")


# GET /ai_insights/ 
@ai_insights_bp.route("/", methods=["GET"])
@login_required
def index():
	
	applications = JobApplication.query\
	.filter_by(
		is_deleted=False,
		user_id=current_user.id
		)\
	.order_by(JobApplication.created_at.desc())\
	.all()

	render_template(
		"ai_insights/index.html",
		applications=applications,
		selected_application=None
	)


# GET /ai_insights/<int:application_id> 
@ai_insights_bp.route("/<int:application_id>", methods=["GET"])
@login_required
def detail(application_id):
	
	applications = JobApplication.query\
	.filter_by(
		is_deleted=False,
		user_id=current_user.id
		)\
	.order_by(JobApplication.created_at.desc())\
	.all()

	selected_application = JobApplication.query\
	.filter_by(
		is_deleted=False,
		id=application_id,
		user_id=current_user.id,
	)\
	.first_or_404()

	render_template(
		"ai_insights/index.html",
		applications=applications,
		selected_application=None
	)
