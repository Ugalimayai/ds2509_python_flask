"""
Python script to act as the signup/registration page to our Flask web application

Author: Karanja
Date: 03-July-2026
"""

# Import the required modules
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField
from wtforms import EmailField, PasswordField, TelField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Declare the RegistrationForm class
class RegistrationForm(FlaskForm):
    names = StringField('Names', validators=[DataRequired()], render_kw={'placeholder': 'Enter your names',
                                                                         'title': 'Please enter your names',
                                                                         'tabindex':10})
    birthdate = DateField('Birthdate', validators=[DataRequired()],
                          render_kw={'placeholder': 'yyyy-mm-dd',
                                     'title': 'Please enter your birthdate',
                                     'tabindex':20})
    gender = RadioField('Gender', choices=['Male', 'Female'],
                        render_kw={'title': 'Please select your gender', 'tabindex':30})
    phone = TelField('Phone number', validators=[DataRequired()],
                     render_kw={'placeholder': '+254712345678',
                                'title': 'Please enter your phone number',
                                'tabindex':40})
    email = EmailField('Email', validators=[DataRequired(), Email()],
                       render_kw={'placeholder': 'me@email.com',
                                  'title': 'Please enter your email',
                                  'tabindex':50})
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)],
                             render_kw={'placeholder': 'Password',
                                        'title': 'Please enter your password','tabindex':60})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),EqualTo('password', message='Passwords must match')],
                                     render_kw={'placeholder': 'Confirm Password',
                                                'tabindex':70})
    # Submit and Reset buttons
    submit = SubmitField('Register',
                         render_kw={'title': 'Submit your registration details',
                                    'tabindex': 80})
    reset = SubmitField('Reset',
                        render_kw={'title': 'Clear all fields',
                                   'tabindex': 90})
