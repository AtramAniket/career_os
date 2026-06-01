from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import JobApplication, MockInterviewSession, MockInterviewQuestion


mock_interviews_bp = Blueprint(
    "mock_interviews",
    __name__,
    url_prefix="/applications/<int:application_id>/mock-interview",
)


@mock_interviews_bp.route("/start", methods=["POST"])
@login_required
def start_mock_interview(application_id):
    application = JobApplication.query.filter_by(
        id=application_id,
        user_id=current_user.id,
        is_deleted=False,
    ).first_or_404()

    session = MockInterviewSession(
        user_id=current_user.id,
        job_application_id=application.id,
        title=f"Mock Interview - {application.role_title}",
        status="active",
    )

    db.session.add(session)
    db.session.flush()

    placeholder_questions = [
        ("behavioral", "Tell me about yourself."),
        ("role_fit", f"Why are you interested in the {application.role_title} role?"),
        ("resume", "Walk me through one project from your resume that is relevant to this role."),
        ("technical", "Tell me about a technical challenge you solved recently."),
        ("closing", "Why should we hire you for this position?"),
    ]

    for index, (category, question_text) in enumerate(placeholder_questions, start=1):
        question = MockInterviewQuestion(
            session_id=session.id,
            category=category,
            question=question_text,
            display_order=index,
        )
        db.session.add(question)

    db.session.commit()

    flash("Mock interview started.", "success")

    return redirect(
        url_for(
            "mock_interviews.view_mock_interview",
            application_id=application.id,
            session_id=session.id,
        )
    )


@mock_interviews_bp.route("/<int:session_id>", methods=["GET"])
@login_required
def view_mock_interview(application_id, session_id):
    application = JobApplication.query.filter_by(
        id=application_id,
        user_id=current_user.id,
        is_deleted=False,
    ).first_or_404()

    session = MockInterviewSession.query.filter_by(
        id=session_id,
        user_id=current_user.id,
        job_application_id=application.id,
    ).first_or_404()

    questions = MockInterviewQuestion.query.filter_by(
        session_id=session.id,
    ).order_by(MockInterviewQuestion.display_order.asc()).all()

    return "Mock interview page coming soon"