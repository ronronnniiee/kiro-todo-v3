"""
Authentication Forms (WTForms).

WTForms handles form rendering and validation for us.
Each form is a Python class where fields are class attributes.
Validators are rules that the form data must pass before it's accepted.

Benefits of using WTForms:
- Automatic CSRF protection (prevents cross-site request forgery attacks)
- Server-side validation (never trust user input!)
- Easy to render in templates with proper HTML attributes
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from app.models import User


class RegistrationForm(FlaskForm):
    """Form for creating a new user account.

    Fields:
        username: 3-80 characters, must be unique
        email: Must be a valid email format, must be unique
        password: Minimum 6 characters
        confirm_password: Must match the password field
    """
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters.')
    ])

    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=6, message='Password must be at least 6 characters long.')
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password.'),
        EqualTo('password', message='Passwords must match.')
    ])

    submit = SubmitField('Register')

    # Custom validators - WTForms automatically calls methods named validate_<fieldname>
    def validate_username(self, username):
        """Check if the username is already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose another.')

    def validate_email(self, email):
        """Check if the email is already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Try logging in instead.')


class LoginForm(FlaskForm):
    """Form for logging into an existing account.

    Fields:
        email: The email address associated with the account
        password: The account password
        remember_me: Whether to keep the user logged in after closing the browser
    """
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.')
    ])

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Log In')
