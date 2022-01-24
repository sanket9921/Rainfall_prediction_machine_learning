from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    DateField,
    SelectField)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    URL
)


class SignupForm(FlaskForm):
    name = StringField(
        'Name',[
            DataRequired(message="Please Enter your name")
        ]
    )
    email = StringField(
        'Email',[
            Email(message="Not a valid email address."),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        [
            DataRequired(message="Please enter a password."),
        ]
    )
    confirmPassword = PasswordField(
        'Repeat Password',
        [
            EqualTo(password,message="Passwords must match")
        ]
    )

