from datetime import datetime, timezone, time

from flask_login import login_required, current_user
from flask import abort, flash, redirect, url_for, Blueprint, render_template

from app import db
from app.helpers import extract_text_from_pdf
from app.services import generate_interview_prep
from app.forms.application_forms import DeleteForm
from app.models import InterviewPrep, JobApplication, ResumeAnalysis, ApplicationDocument

interview_prep_bp = Blueprint(
	"interview_prep",
	__name__,
	url_prefix="/applications/<int:application_id>/interview_prep")


# GET "/applications/1/interview_prep/"
@interview_prep_bp.route("/", methods=["GET"])
@login_required
def detail(application_id):

	csrf_token = DeleteForm()

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
	.first()

	prep_history = InterviewPrep.query\
	.filter_by(job_application_id=application.id)\
	.order_by(InterviewPrep.created_at.desc())\
	.all()

	return render_template(
		"interview_prep/detail.html",
		csrf_token=csrf_token,
		application=application,
		latest_prep=latest_prep,
		prep_history=prep_history,
	)


# GET "/applications/1/interview_prep/generate"
@interview_prep_bp.route("/generate", methods=["POST"])
@login_required
def generate(application_id):

	application = JobApplication.query\
	.filter_by(
		id=application_id,
		user_id=current_user.id,
		is_deleted=False)\
	.first_or_404()

	today_start = datetime.combine(
	    datetime.now(timezone.utc).date(),
	    time.min,
	    tzinfo=timezone.utc,
	)

	today_prep_count = InterviewPrep.query.filter(
	    InterviewPrep.job_application_id == application.id,
	    InterviewPrep.created_at >= today_start,
	).count()

	if today_prep_count >= 2:
	    flash("Daily interview prep generation limit reached. Try again tomorrow.", "warning")
	    return redirect(url_for("interview_prep.detail", application_id=application.id))

	latest_analysis = ResumeAnalysis.query\
	.filter_by(
		job_application_id=application.id,
		is_latest=True)\
	.order_by(ResumeAnalysis.created_at.desc())\
	.first()

	if not latest_analysis:
		flash("Generate a resume analysis before creating interview prep.", "warning")
		return(redirect(url_for("interview_prep.detail", application_id=application_id)))

	primary_resume = ApplicationDocument.query\
	.filter_by(
		job_application_id=application.id,
		is_primary=True)\
	.order_by(ApplicationDocument.uploaded_at.desc())\
	.first()

	if not primary_resume:
		flash("Please set primary resume before generating interview prep.", "warning")
		return(redirect(url_for("interview_prep.detail", application_id=application_id)))

	resume_text = extract_text_from_pdf(primary_resume.filepath)

	if not resume_text:
		flash("Resume text is missing. Please re-uplaod or re-analyze resume first", "warning")
		return(redirect(url_for("interview_prep.detail", application_id=application_id)))

	InterviewPrep.query\
	.filter_by(
		job_application_id=application.id,
		is_latest=True)\
	.update({"is_latest": False})

	try:
	    prep_data = generate_interview_prep(
	        application=application,
	        resume_text=resume_text,
	        resume_analysis=latest_analysis.analysis_summary,
	    )
	except Exception:
	    flash("Interview prep could not be generated right now. Please try again.", "warning")
	    return redirect(url_for("interview_prep.detail", application_id=application.id))

	# prep_data = generate_interview_prep(
	# 	application=application,
	# 	resume_text=resume_text,
	# 	resume_analysis=latest_analysis.analysis_summary)

	interview_prep = InterviewPrep(
		job_application_id=application.id,
		resume_id=primary_resume.id,
		strategy_summary=prep_data.get("strategy_summary"),
		questions_json = prep_data,
		is_latest=True
		)

	db.session.add(interview_prep)
	db.session.commit()

	flash("Interview pep summary generated successfully.", "success")
	return(redirect(url_for("interview_prep.detail", application_id=application_id)))