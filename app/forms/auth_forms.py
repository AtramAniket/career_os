from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models.user import User

class SignupForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])

	email = StringField("Email", validators=[DataRequired(), Email(), Length(max=150)])

	passord = PasswordField("Password", validators=[DataRequired(), Length(min=6)])

	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("passord")])

	submit = SubmitField("Create Account")


	def validate_username(self, username):
		existing_user = User.query.filter_by(username=username.data).first()
		if existing_user:
			raise ValidationError("Username is already taken.")

	def validate_email(self, email):
		existing_user = User.query.filter_by(email = email.data.lower()).first()
		if existing_user:
			raise ValidationError("This email is already registered.")


class LoginForm(FlaskForm):
	identifier = StringField("Username or Email", validators=[DataRequired()])

	passord = PasswordField("Password", validators=[DataRequired()])

	submit = SubmitField("Login")