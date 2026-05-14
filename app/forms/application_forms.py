from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional, Length

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

	submit = SubmitField("Save Application")