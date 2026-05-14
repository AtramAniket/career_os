from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
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

	job_link = StringField(
		"Job Link",
		validators=[Optional(), Length(max=500)]
		)

	location = StringField(
		"Location",
		validators=[Optional(), Length(max=120)]
		)

	status = SelectField(
		"Status",
		validators=[DataRequired()],
		choices=[
		("saved", "Saved"),
		("applied", "Applied"),
		("interviewing", "Interviewing"),
		("offer", "Offer"),
		("rejected", "Rejected"),
		("archived", "Archived")]
		)

	source = StringField(
		"Source",
		validators=[Optional(), Length(max=120)]
		)

	notes = TextAreaField(
		"Notes",
		validators=[Optional()]
		)

	submit = SubmitField("Save Application")