from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms.validators import DataRequired, Optional, Length
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField, SubmitField


class JobApplicationForm(FlaskForm):

	company_name = StringField(
		"Company Name",
		validators=[DataRequired(), Length(max=120)]
		)

	role_title = StringField(
		"Role Title",
		validators=[DataRequired(), Length(max=120)]
		)

	job_url = StringField(
		"Job URL",
		validators=[Optional(), Length(max=500)]
		)

	location = StringField(
		"Location",
		validators=[Optional(), Length(max=120)]
		)

	work_mode = SelectField(
		"Work Mode",
		validators=[DataRequired()],
		choices=[
		("REMOTE", "Remote"),
		("HYBRID", "Hybrid"),
		("ONSITE", "On-Site")]
		)

	employment_type = SelectField(
		"Employment Type",
		validators=[DataRequired()],
		choices=[
		("FULL_TIME", "Full-Time"),
		("PART_TIME", "Part-Time"),
		("INTERNSHIP", "Internship"),
		("CONTRACT", "Contract")]
		)

	salary_min = IntegerField(
		"Minimum Expected Salary",
		validators=[Optional()])

	salary_max = IntegerField(
		"Maximum Expected Salary",
		validators=[Optional()])

	source = StringField(
		"Source",
		validators=[Optional(), Length(max=120)]
		)

	status = SelectField(
		"Status",
		validators=[DataRequired()],
		choices=[
		("SAVED", "Saved"),
		("APPLIED", "Applied"),
		("ASSESSMENT", "Assessment"),
		("INTERVIEW", "Interview"),
		("OFFER", "Offer"),
		("REJECTED", "Rejected"),
		("GHOSTED", "Ghosted")]
		)

	priority = SelectField(
		"Priority",
		validators=[DataRequired()],
		choices=[
		("LOW", "Low"),
		("MEDIUM", "Medium"),
		("HIGH", "High"),]
		)

	date_applied = DateField(
		"Applied On",
		validators=[Optional()])

	deadline = DateField(
		"Application Deadline",
		validators=[Optional()])

	notes = TextAreaField(
		"Notes",
		validators=[Optional()]
		)

	job_description = TextAreaField(
		"Job Description",
		validators=[Optional()]
	)

	resume_notes = TextAreaField(
		"Resume Notes",
		validators=[Optional()]
	)

	submit = SubmitField("Save Application")


class ApplicationEventForm(FlaskForm):

	title = StringField(
		"Event Title",
		validators=[DataRequired(), Length(max=120)]
		)

	event_type = SelectField(
		"Event Type",
		choices=[
		("SAVED", "Saved"),
		("APPLIED", "Applied"),
		("ASSESSMENT", "Assessment"),
		("INTERVIEW", "Interview"),
		("OFFER", "Offer"),
		("REJECTED", "Rejected"),
		("GHOSTED", "Ghosted")],
		validators=[DataRequired()]
		)

	event_date = DateField(
		"Event Date",
		default=date.today(),
		validators=[DataRequired()]
		)

	description = TextAreaField(
		"Description",
		validators=[Optional()],
		)

	submit = SubmitField("Add Event")


class DocumentUploadForm(FlaskForm):

	document_type = SelectField(
		"Document Type",
		choices=[
			("other", "Other"),
			("resume", "Resume"),
			("portfolio", "Portfolio"),
			("certificate", "Certificate"),
			("cover_letter", "Cover Letter")
		],
		validators=[DataRequired()]
	)

	document = FileField(
		"Upload Document",
		validators=[FileRequired()]
	)

	notes = TextAreaField(
		"Notes",
		validators=[Optional(), Length(max=500)]
	)

	submit = SubmitField("Upload Document")

class DeleteForm(FlaskForm):
	pass