from flask import Blueprint, render_template
from flask_login import login_required, current_user

from sqlalchemy import desc, func

from app.extensions import db
from app.models import JobApplication, JobStatus


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def index():
    total_applications = (
        JobApplication.query
        .filter_by(user_id=current_user.id, is_deleted=False)
        .count()
    )

    status_counts = (
        db.session.query(JobApplication.status, func.count(JobApplication.id))
        .filter(
            JobApplication.user_id == current_user.id,
            JobApplication.is_deleted == False,
        )
        .group_by(JobApplication.status)
        .all()
    )

    counts = {
        status.value: count
        for status, count in status_counts
    }

    active_count = (
        counts.get("Saved", 0)
        + counts.get("Applied", 0)
        + counts.get("Assessment", 0)
    )

    interview_count = counts.get("Interview", 0)

    closed_count = (
        counts.get("Rejected", 0)
        + counts.get("Ghosted", 0)
        + counts.get("Offer", 0)
    )

    recent_applications = (
        JobApplication.query
        .filter_by(user_id=current_user.id, is_deleted=False)
        .order_by(desc(JobApplication.created_at))
        .limit(6)
        .all()
    )

    return render_template(
        "dashboard.html",
        counts=counts,
        JobStatus=JobStatus,
        total_applications=total_applications,
        active_count=active_count,
        interview_count=interview_count,
        closed_count=closed_count,
        recent_applications=recent_applications,
    )
