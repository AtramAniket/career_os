import os
from uuid import uuid4
from datetime import datetime, timezone
from werkzeug.utils import secure_filename

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file, abort

from app.extensions import db
from app.helpers import allowed_document_file
from app.models import JobApplication, ApplicationEvent, JobStatus, ApplicationDocument, ResumeAnalysis
from app.forms.application_forms import JobApplicationForm, ApplicationEventForm, DeleteForm, DocumentUploadForm


applications_bp = Blueprint("applications", __name__, url_prefix="/applications")


@applications_bp.route("/")
@login_required
def index():

	search_query = request.args.get("q", "").strip()
	status_filter = request.args.get("status", "").strip()

	query = JobApplication.query\
	.filter_by(user_id=current_user.id, is_deleted=False)\

	if search_query:
		query = query\
		.filter(
			db.or_(
				JobApplication.source.ilike(f"%{search_query}%"),
				JobApplication.location.ilike(f"%{search_query}%"),
				JobApplication.role_title.ilike(f"%{search_query}%"),
				JobApplication.company_name.ilike(f"%{search_query}%"),
				)
			)

	if status_filter:
		query = query.filter(JobApplication.status == JobStatus[status_filter])

	job_applications = query\
	.order_by(JobApplication.created_at.desc())\
	.all()

	return render_template(
		"applications/index.html", 
		job_applications=job_applications,
		search_query=search_query,
		status_filter=status_filter,
		JobStatus=JobStatus
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
			notes = form.notes.data,
			job_description = form.job_description.data,
			resume_notes = form.resume_notes.data
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
	delete_form = DeleteForm()
	upload_form = DocumentUploadForm()

	if form.validate_on_submit():
		event = ApplicationEvent(
		    job_application_id=application_id,
		    title=form.title.data,
		    event_date=form.event_date.data,
		    description=form.description.data,
		    event_type=form.event_type.data,
		)

		selected_event_type = form.event_type.data

		status_event_map = {
		    "SAVED": JobStatus.SAVED,
		    "APPLIED": JobStatus.APPLIED,
		    "ASSESSMENT": JobStatus.ASSESSMENT,
		    "INTERVIEW": JobStatus.INTERVIEW,
		    "REJECTED": JobStatus.REJECTED,
		    "GHOSTED": JobStatus.GHOSTED,
		    "OFFER": JobStatus.OFFER,
		}

		if selected_event_type in status_event_map:
		    application.status = status_event_map[selected_event_type]

		db.session.add(event)
		db.session.add(application)
		db.session.commit()

		flash("Application event added successfully", "success")
		return redirect(url_for("applications.detail", application_id=application.id))

	events = (
		ApplicationEvent.query\
		.filter_by(job_application_id = application.id)\
		.order_by(ApplicationEvent.event_date.desc())\
		.all()
		)

	documents = (
	    ApplicationDocument.query\
	    .filter_by(job_application_id=application.id)\
	    .order_by(ApplicationDocument.uploaded_at.desc())\
	    .all()
	)

	latest_analysis = ResumeAnalysis.query.filter_by(
		is_latest=True,
		analysis_type="resume_review",
	    job_application_id=application.id
	).order_by(
	    ResumeAnalysis.created_at.desc()
	).first()

	latest_tailoring_analysis = ResumeAnalysis.query.filter_by(
	    job_application_id=application.id,
	    is_latest=True,
	    analysis_type="tailoring",
	).order_by(
	    ResumeAnalysis.created_at.desc()
	).first()

	return render_template(
		"applications/detail.html",
		form=form,
		events=events,
		application=application,
		delete_form=delete_form,
		upload_form=upload_form,
		documents=documents,
		latest_analysis=latest_analysis,
		latest_tailoring_analysis=latest_tailoring_analysis,
		)


@applications_bp.route("/<int:application_id>/documents/upload", methods=["POST"])
@login_required
def upload_document(application_id):
    application = (
        JobApplication.query
        .filter_by(id=application_id, user_id=current_user.id, is_deleted=False)
        .first_or_404()
    )

    form = DocumentUploadForm()

    if not form.validate_on_submit():
        flash("Please select a valid document.", "danger")
        return redirect(url_for("applications.detail", application_id=application.id))

    file = form.document.data

    if not file or file.filename == "":
        flash("Please choose a file to upload.", "danger")
        return redirect(url_for("applications.detail", application_id=application.id))

    if not allowed_document_file(file.filename):
        flash("Only PDF, DOC, DOCX, and TXT files are allowed.", "danger")
        return redirect(url_for("applications.detail", application_id=application.id))

    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit(".", 1)[1].lower()
    stored_filename = f"{uuid4().hex}.{extension}"

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, stored_filename)
    file.save(file_path)

    file_size =os.path.getsize(file_path) 
    mime_type = file.mimetype
    notes = form.notes.data

    document = ApplicationDocument(
        job_application_id=application.id,
        document_type=form.document_type.data,
        original_filename=original_filename,
        stored_filename=stored_filename,
        filepath=file_path,
        file_size=file_size,
        mime_type=mime_type,
        notes=notes
    )

    db.session.add(document)
    db.session.commit()

    flash("Document uploaded successfully.", "success")
    return redirect(url_for("applications.detail", application_id=application.id))


@applications_bp.route("/documents/<int:document_id>/download", methods=["GET"])
@login_required
def download_document(document_id):
    document = (
        ApplicationDocument.query
        .join(JobApplication)
        .filter(
            ApplicationDocument.id == document_id,
            JobApplication.user_id == current_user.id,
            JobApplication.is_deleted == False,
        )
        .first_or_404()
    )

    if not os.path.exists(document.filepath):
        flash("This document record exists, but the file is missing from storage.", "warning")
        return redirect(url_for("applications.detail", application_id=document.job_application_id))

    return send_file(
        document.filepath,
        as_attachment=False,
        download_name=document.original_filename,
    )


@applications_bp.route("/documents/<int:document_id>/delete", methods=["POST"])
@login_required
def delete_document(document_id):
    document = (
        ApplicationDocument.query
        .join(JobApplication)
        .filter(
            ApplicationDocument.id == document_id,
            JobApplication.user_id == current_user.id,
            JobApplication.is_deleted == False,
        )
        .first_or_404()
    )

    application_id = document.job_application_id

    if document.filepath and os.path.exists(document.filepath):
        os.remove(document.filepath)

    db.session.delete(document)
    db.session.commit()

    flash("Document deleted successfully.", "success")
    return redirect(url_for("applications.detail", application_id=application_id))


@applications_bp.route("/documents/<int:document_id>/set-primary", methods=["POST"])
@login_required
def set_primary_document(document_id):
    document = ApplicationDocument.query.get_or_404(document_id)

    application = document.application

    if application.user_id != current_user.id:
        abort(403)

    if document.document_type != "resume":
        flash("Only resume documents can be marked as primary.", "warning")
        return redirect(url_for("applications.detail", application_id=application.id))

    ApplicationDocument.query.filter_by(
        job_application_id=application.id,
        document_type="resume"
    ).update({"is_primary": False})

    document.is_primary = True

    db.session.commit()

    flash("Primary resume updated.", "success")
    return redirect(url_for("applications.detail", application_id=application.id))


@applications_bp.route("/<int:application_id>/delete", methods=["POST"])
@login_required
def delete_application(application_id):

	application = (JobApplication.query\
		.filter_by(id=application_id, user_id=current_user.id)\
		.first_or_404())

	application.is_deleted = True
	application.deleted_at = datetime.now(timezone.utc)

	db.session.commit()
	flash("Job application deleted successfully", "success")

	return redirect(url_for("applications.index"))