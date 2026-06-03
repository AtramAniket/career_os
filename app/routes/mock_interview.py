import random
from datetime import datetime, timezone, time

from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.services import evaluate_mock_session
from app.forms.application_forms import DeleteForm
from app.models import (
    JobApplication,
    InterviewPrep,
    MockInterviewSession,
    MockInterviewQuestion,
    MockInterviewResponse,
)


mock_interviews_bp = Blueprint(
    "mock_interviews",
    __name__,
    url_prefix="/applications/<int:application_id>/mock-interview",
)


def _flatten_prep_questions(prep_data):
    question_bank = []

    categories = [
        ("hr", "hr_questions"),
        ("technical", "technical_questions"),
        ("project", "project_questions"),
        ("resume", "resume_based_questions"),
        ("gap_probe", "red_flags_to_prepare_for"),
    ]

    for category, key in categories:
        questions = prep_data.get(key, [])

        if not isinstance(questions, list):
            continue

        for item in questions:
            if not isinstance(item, dict):
                continue

            question_text = item.get("question")

            if not question_text:
                continue

            question_bank.append({
                "category": category,
                "question": question_text,
            })

    return question_bank


@mock_interviews_bp.route("/start", methods=["POST"])
@login_required
def start_mock_interview(application_id):
    application = JobApplication.query.filter_by(
        id=application_id,
        user_id=current_user.id,
        is_deleted=False,
    ).first_or_404()

    latest_prep = InterviewPrep.query.filter_by(
        job_application_id=application.id,
        is_latest=True,
    ).order_by(InterviewPrep.created_at.desc()).first()

    if not latest_prep or not latest_prep.questions_json:
        flash("Generate interview prep questions before starting a mock interview.", "warning")
        return redirect(
            url_for(
                "interview_prep.detail",
                application_id=application.id,
            )
        )

    question_bank = _flatten_prep_questions(latest_prep.questions_json)

    if not question_bank:
        flash("No interview prep questions found. Please regenerate interview prep.", "warning")
        return redirect(
            url_for(
                "interview_prep.detail",
                application_id=application.id,
            )
        )

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

    today_start = datetime.combine(
        datetime.now(timezone.utc).date(),
        time.min,
        tzinfo=timezone.utc,
    )

    today_session_count = MockInterviewSession.query.filter(
        MockInterviewSession.user_id == current_user.id,
        MockInterviewSession.job_application_id == application.id,
        MockInterviewSession.created_at >= today_start,
    ).count()

    if today_session_count >= 2:
        flash("You have reached today's mock interview limit for this application.", "warning")
        return redirect(
            url_for(
                "interview_prep.detail",
                application_id=application.id,
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

    random.shuffle(question_bank)
    selected_questions = question_bank

    for index, question_data in enumerate(selected_questions, start=1):
        question = MockInterviewQuestion(
            session_id=session.id,
            category=question_data.get("category", "general"),
            question=question_data.get("question", ""),
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

    current_question = None

    for question in questions:
        if question.id not in answered_questions_ids:
            current_question = question
            break

    return render_template(
        "mock_interviews/detail.html",
        application=application,
        session=session,
        questions=questions,
        current_question=current_question,
        answered_count=len(answered_questions_ids),
        total_questions=len(questions),
        form=form,
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

    existing_response = MockInterviewResponse.query.filter_by(
        question_id=question.id,
    ).first()

    if existing_response:
        flash("This question has already been answered.", "warning")
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
    db.session.flush()

    total_questions = MockInterviewQuestion.query.filter_by(
        session_id=session.id,
    ).count()

    answered_count = MockInterviewResponse.query.join(MockInterviewQuestion).filter(
        MockInterviewQuestion.session_id == session.id,
    ).count()

    if answered_count >= total_questions:
        session.status = "completed"
        session.completed_at = datetime.now(timezone.utc)

        responses = (
            MockInterviewResponse.query
            .join(MockInterviewQuestion)
            .filter(MockInterviewQuestion.session_id == session.id)
            .order_by(MockInterviewQuestion.display_order.asc())
            .all()
        )

        qa_pairs = []

        for item in responses:
            qa_pairs.append({
                "question_id": item.question_id,
                "question": item.question.question,
                "category": item.question.category,
                "answer": item.answer,
            })

        try:
            evaluation_result = evaluate_mock_session(
                role_title=application.role_title,
                company_name=application.company_name,
                qa_pairs=qa_pairs,
            )

            evaluations = evaluation_result.get("evaluations", [])

            evaluations_by_question_id = {
                evaluation.get("question_id"): evaluation
                for evaluation in evaluations
            }

            for item in responses:
                evaluation = evaluations_by_question_id.get(item.question_id)

                if not evaluation:
                    continue

                item.ai_score = evaluation.get("ai_score")
                item.ai_feedback = evaluation.get("ai_feedback")
                item.ai_improved_answer = evaluation.get("ai_improved_answer")
                item.evaluated_at = datetime.now(timezone.utc)

        except Exception:
            flash("Interview completed, but AI feedback could not be generated right now.", "warning")

    db.session.commit()

    flash("Answer saved.", "success")

    return redirect(
        url_for(
            "mock_interviews.view_mock_interview",
            application_id=application.id,
            session_id=session.id,
        )
    )


@mock_interviews_bp.route("/<int:session_id>/review", methods=["GET"])
@login_required
def review_mock_interview(application_id, session_id):

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

    responses = MockInterviewResponse.query\
    .join(MockInterviewQuestion)\
    .filter(
        MockInterviewQuestion.session_id == session.id,
    )\
    .order_by(MockInterviewQuestion.display_order.asc())\
    .all()

    scored_responses = [response for response in responses if response.ai_score is not None]

    average_score = None

    if scored_responses:
        average_score = round(
            sum(response.ai_score for response in scored_responses) / len(scored_responses),
            1
        )

    category_scores = {}

    for response in scored_responses:
        category = response.question.category or "general"

        if category not in category_scores:
            category_scores[category] = {
                "total": 0,
                "count": 0,
                "average": 0,
            }

        category_scores[category]["total"] += response.ai_score
        category_scores[category]["count"] += 1

    for category, data in category_scores.items():
        data["average"] = round(data["total"] / data["count"], 1)

    return render_template(
        "mock_interviews/review.html",
        session=session,
        responses=responses,
        application=application,
        average_score=average_score,
        category_scores=category_scores,
    )


@mock_interviews_bp.route("/history", methods=["GET"])
@login_required
def mock_interview_history(application_id):
    
    application = JobApplication.query.filter_by(
        id=application_id,
        user_id=current_user.id,
        is_deleted=False,
    ).first_or_404()

    sessions = MockInterviewSession.query.filter_by(
        id=session_id,
        user_id=current_user.id,
        job_application_id=application.id,
    ).all()

    return render_template(
        "mock_interviews/history.html",
        application=application,
        sessions=sessions
    )