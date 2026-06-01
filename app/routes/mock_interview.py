from datetime import datetime, timezone

from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from app.forms.application_forms import DeleteForm

from app.extensions import db
from app.models import(
    JobApplication,
    MockInterviewSession,
    MockInterviewQuestion,
    MockInterviewResponse)


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

    existing_session = MockInterviewSession.query.filter_by(
        user_id=current_user.id,
        job_application_id=application.id,
        status="active",
    ).order_by(MockInterviewSession.created_at.desc()).first()

    if existing_session:
        return redirect(
            url_for(
                "mock_interviews.view_mock_interview",
                application_id=application.id,
                session_id=existing_session.id,
            )
        )

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

    form = DeleteForm()

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

    answered_questions_ids = {
        response.question_id
        for question in questions
        for response in question.mock_interview_responses
    }

    current_question=None

    for question in questions:
        if question.id not in answered_questions_ids:
            current_question=question
            break

    return render_template(
        "mock_interviews/detail.html",
        application=application,
        session=session,
        questions=questions,
        current_question=current_question,
        answered_count=len(answered_questions_ids),
        total_questions=len(questions),
        form=form
    )


@mock_interviews_bp.route("/<int:session_id>/questions/<int:question_id>/answer", methods=["POST"])
@login_required
def submit_answer(application_id, session_id, question_id):

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

    question = MockInterviewQuestion.query.filter_by(
        id=question_id,
        session_id=session.id,
    ).first_or_404()

    answer = request.form.get("answer", "").strip()

    if not answer:
        flash("Please write an answer before submitting.", "warning")
        return redirect(
            url_for(
                "mock_interviews.view_mock_interview",
                application_id=application.id,
                session_id=session.id,
            )
        )

    response = MockInterviewResponse(
        question_id=question.id,
        answer=answer,
    )

    db.session.add(response)

    total_questions = MockInterviewQuestion.query.filter_by(
        session_id=session.id
    ).count()

    answered_count = MockInterviewResponse.query.join(MockInterviewQuestion).filter(
        MockInterviewQuestion.session_id == session.id
    ).count()

    if answered_count >= total_questions:
        session.status = "completed"
        session.completed_at = datetime.now(timezone.utc)

    db.session.commit()

    flash("Answer saved.", "success")

    return redirect(
        url_for(
            "mock_interviews.view_mock_interview",
            application_id=application.id,
            session_id=session.id,
        )
    )