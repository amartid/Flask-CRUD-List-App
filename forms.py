from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp
class AddPersonForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z ]+$', message='Name must contain only letters and spaces.')
    ])
    submit = SubmitField('Add Person')