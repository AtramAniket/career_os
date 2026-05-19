from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.forms.application_forms import JobApplicationForm, ApplicationEventForm
from app.models import JobApplication, ApplicationEvent

applications_bp = Blueprint("applications", __name__, url_prefix="/applications")

@applications_bp.route("/")
@login_required
def index():

	job_applications = JobApplication.query\
	.filter_by(user_id=current_user.id)\
	.order_by(JobApplication.created_at.desc())\
	.all()

	return render_template(
		"applications/index.html", 
		job_applications=job_applications
		)


@applications_bp.route("/new", methods=["GET","POST"])
@login_required
def create():

	form = JobApplicationForm()

	if form.validate_on_submit():

		job_application = JobApplication(
			user_id = current_user.id,
			company_name = form.company_name.data,
			role_title = form.role_title.data,
			job_url = form.job_url.data,
			location = form.location.data,
			work_mode = form.work_mode.data,
			employment_type = form.employment_type.data,
			salary_min = form.salary_min.data,
			salary_max = form.salary_max.data,
			status = form.status.data,
			priority = form.priority.data,
			date_applied = form.date_applied.data,
			deadline = form.deadline.data,
			source = form.source.data,
			notes = form.notes.data
			)

		db.session.add(job_application)
		db.session.commit()

		flash("Job Application Added Successfully", "success")
		return redirect(url_for("applications.index"))

	return render_template(
		"applications/create.html",
		form=form
		)


@applications_bp.route("/<int:application_id>", methods=["GET", "POST"])
@login_required
def detail(application_id):

	application = (JobApplication.query\
		.filter_by(id=application_id, user_id=current_user.id)\
		.first_or_404())

	form = ApplicationEventForm()

	if form.validate_on_submit():
		event = ApplicationEvent(
			job_application_status = application_id,
			title = form.title.data,
			event_date = form.event_date.data,
			description = form.description.data,
			event_type = form.event_type.data,
		)

		db.session.add(event)
		db.session.commit()

		flash("Application event added successfully", "success")
		return redirect(url_for("applications.detail", application_id=application.id))

	events = (
		ApplicationEvent.query\
		.filter_by(job_application_status = application.id)\
		.order_by(ApplicationEvent.event_date.desc())\
		.all()
		)

	return render_template(
		"applications/detail.html",
		form=form,
		events=events,
		application=application
		)