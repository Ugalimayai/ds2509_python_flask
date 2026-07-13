# Python script for the product form

# Import the required models
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired

# Create the product form
class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])