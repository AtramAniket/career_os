from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models import (
    ApplicationDocument,
    InterviewPrep,
    JobApplication,
    ResumeAnalysis,
)


ai_insights_bp = Blueprint("ai_insights", __name__, url_prefix="/ai_insights")


@ai_insights_bp.route("/", methods=["GET"])
@login_required
def index():
    applications = (
        JobApplication.query
        .filter_by(
            is_deleted=False,
            user_id=current_user.id,
        )
        .order_by(JobApplication.created_at.desc())
        .all()
    )

    return render_template(
        "ai_insights/index.html",
        applications=applications,
        selected_application=None,
        primary_resume=None,
        latest_analysis=None,
        latest_tailoring_analysis=None,
        latest_interview_prep=None,
    )


@ai_insights_bp.route("/<int:application_id>", methods=["GET"])
@login_required
def detail(application_id):
    applications = (
        JobApplication.query
        .filter_by(
            is_deleted=False,
            user_id=current_user.id,
        )
        .order_by(JobApplication.created_at.desc())
        .all()
    )

    selected_application = (
        JobApplication.query
        .filter_by(
            is_deleted=False,
            id=application_id,
            user_id=current_user.id,
        )
        .first_or_404()
    )

    primary_resume = (
        ApplicationDocument.query
        .filter_by(
            job_application_id=selected_application.id,
            document_type="resume",
            is_primary=True,
        )
        .first()
    )

    latest_analysis = (
        ResumeAnalysis.query
        .filter_by(
            job_application_id=selected_application.id,
            analysis_type="resume_review",
            is_latest=True,
        )
        .order_by(ResumeAnalysis.created_at.desc())
        .first()
    )

    latest_tailoring_analysis = (
        ResumeAnalysis.query
        .filter_by(
            job_application_id=selected_application.id,
            analysis_type="tailoring",
            is_latest=True,
        )
        .order_by(ResumeAnalysis.created_at.desc())
        .first()
    )

    latest_interview_prep = (
        InterviewPrep.query
        .filter_by(
            job_application_id=selected_application.id,
            is_latest=True,
        )
        .order_by(InterviewPrep.created_at.desc())
        .first()
    )

    return render_template(
        "ai_insights/index.html",
        applications=applications,
        selected_application=selected_application,
        primary_resume=primary_resume,
        latest_analysis=latest_analysis,
        latest_tailoring_analysis=latest_tailoring_analysis,
        latest_interview_prep=latest_interview_prep,
    )