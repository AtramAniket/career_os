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
    .limit(8)\
    .all()

    recent_events = ApplicationEvent.query\
    .join(JobApplication)\
    .filter_by(user_id=current_user.id, is_deleted=False)\
    .order_by(desc(ApplicationEvent.created_at), desc(ApplicationEvent.created_at))\
    .limit(8)\
    .all()

    interview_count = counts.get("Interview", 0)
    closed_count = counts.get("Rejected", 0) + counts.get("Ghosted", 0) + counts.get("Offer", 0)
    active_count = counts.get("Saved", 0) + counts.get("Applied", 0) + counts.get("Assessment", 0)
   
    return render_template(
        "dashboard.html",
        counts=counts,
        JobStatus=JobStatus,
        active_count=active_count,
        closed_count=closed_count,
        recent_events=recent_events,
        interview_count=interview_count,
        total_applications=total_applications,
        recent_applications=recent_applications)