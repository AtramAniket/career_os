from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func, desc

from app.extensions import db
from app.models import JobApplication, ApplicationEvent, JobStatus

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def index():

    total_applications = JobApplication.query\
    .filter_by(user_id=current_user.id, is_deleted=False)\
    .count()

    status_counts = (
        db.session.query(JobApplication.status, func.count(JobApplication.id))\
        .filter(JobApplication.user_id == current_user.id, JobApplication.is_deleted==False)\
        .group_by(JobApplication.id)\
        .all()
        )

    counts = {status.value:count for status, count in status_counts}

    recent_applications = JobApplication.query\
    .filter_by(user_id=current_user.id, is_deleted=False)\
    .order_by(desc(JobApplication.created_at))\
    .limit(5)\
    .all()

    recent_events = ApplicationEvent.query\
    .join(JobApplication)\
    .filter_by(user_id=current_user.id, is_deleted=False)\
    .order_by(desc(JobApplication.created_at))\
    .limit(5)\
    .all()

    return render_template(
        "dashboard.html",
        total_applications=total_applications,
        counts=counts,
        recent_applications=recent_applications,
        recent_events=recent_events,
        JobStatus=JobStatus)