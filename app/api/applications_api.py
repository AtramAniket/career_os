from flask import jsonify
from flask_login import login_required, current_user

from app.api import api_bp
from app.models import JobApplication
from app.utils.serializers import serialize_application

@api_bp.route("/applications")
@login_required
def get_applications():

	applications = JobApplication.query\
	.filter_by(
		user_id=current_user.id,
		is_deleted=False
		)\
	.order_by(JobApplication.created_at.desc())\
	.all()

	return jsonify(
		{
			"applications": [serialize_application(application) for application in applications]
		}
	)

@api_bp.get("/applications/<int:application_id>")
@login_required
def get_application(application_id):
    application = (
        JobApplication.query
        .filter_by(
            id=application_id,
            user_id=current_user.id,
            is_deleted=False,
        )
        .first_or_404()
    )

    return jsonify({
        "application": serialize_application(application)
    })