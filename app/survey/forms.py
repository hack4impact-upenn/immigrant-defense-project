from flask_wtf import Form
from wtforms.fields import RadioField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

from app import db
from app.models import SurveyOption


def generate_response_form(question):
    """Dynamically creates a response form for a survey question."""
    class SurveyResponseForm(Form):
        response = RadioField(
            question.content,
            choices=[(str(o.id), o.content) for o in SurveyOption.query.filter_by(question_id=question.id)],
            validators=[InputRequired()]
        )
        submit = SubmitField('Next')

    return SurveyResponseForm()


class NewSurveyQuestion(Form):
    content = StringField('Question', validators=[InputRequired()])
    description = TextAreaField('Description')
    submit = SubmitField()
