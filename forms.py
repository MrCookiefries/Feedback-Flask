from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email

class RegisterUserForm(FlaskForm):
    """form for registering a user"""
    username = StringField("Username", validators=[
        InputRequired(message="You must have a username."),
        Length(min=5, max=20, message="Username must be between %(min)d & %(max)d characters long.")
    ])
    password = PasswordField("Password", validators=[
        InputRequired(message="You must have a password."),
        Length(min=6, message="Password must be longer than %(min)d characters.")
    ])
    email = EmailField("Email", validators=[
        InputRequired(message="You must have an email."),
        Length(max=50, message="Email cannot be longer than %(max)d characters."),
        Email(message="Email must be a valid email.")
    ])
    first_name = StringField("First Name", validators=[
        InputRequired(message="You must have an first name."),
        Length(max=30, message="First name cannot be longer than %(max)d characters.")
    ])
    last_name = StringField("Last Name", validators=[
        InputRequired(message="You must have an last name."),
        Length(max=30, message="Last name cannot be longer than %(max)d characters.")
    ])

class LoginUserForm(FlaskForm):
    """form for logging in a user"""
    username = StringField("Username", validators=[
        InputRequired(message="You must have a username."),
        Length(min=5, max=20, message="Username must be between %(min)d & %(max)d characters long.")
    ])
    password = PasswordField("Password", validators=[
        InputRequired(message="You must have a password."),
        Length(min=6, message="Password must be longer than %(min)d characters.")
    ])

class FeedbackForm(FlaskForm):
    """form for creating feedback"""
    title = StringField("Title", validators=[
        InputRequired(message="You must have an title."),
        Length(max=100, message="A title cannot be longer than %(max)d characters.")
    ])
    content = TextAreaField("Content", validators=[
        InputRequired(message="You must have some content.")
    ])

