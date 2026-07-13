"""
Python script to act as the login/sign-in page to our Flask web application

Author: Karanja
Date: 04-July-2026
"""

# Import the required modules
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms import EmailField, PasswordField, TelField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Declare the RegistrationForm class
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()],
                       render_kw={'placeholder': 'me@email.com',
                                  'title': 'Please enter your email',
                                  'tabindex': 10})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)],
                             render_kw={'placeholder': 'Password',
                                        'title': 'Please enter your password', 'tabindex': 20})
    # Optional 'Remember Me' checkbox
    remember_me = BooleanField('Remember Me')

    #Submit Button
    submit = SubmitField('Log In',
                         render_kw={'title': 'Log In/Sign-in to the site', 'tabindex': 30})