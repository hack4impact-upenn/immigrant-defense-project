from flask_wtf import Form
from wtforms.fields import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

from app import db
from app.models import SurveyQuestion


class NewSurveyQuestion(Form):
    content = StringField('Question', validators=[InputRequired()])
    description = TextAreaField('Description')
    type = SelectField('Type',
        choices=SurveyQuestion.type_choices(),
        validators=[InputRequired()])
    screen = SelectField('Is this a screening question?',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        default='No')
    submit = SubmitField()
