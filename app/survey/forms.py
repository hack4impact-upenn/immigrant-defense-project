from flask_wtf import Form
from wtforms.fields import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

from app import db
from app.models import SurveyQuestion


class NewSurveyQuestion(Form):
    content = StringField('Question', validators=[InputRequired()])
    description = TextAreaField('Description')
    submit = SubmitField()
