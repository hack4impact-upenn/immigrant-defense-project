from flask_wtf import Form
from wtforms.fields import (
    StringField,
    SubmitField
)
from wtforms.validators import (
    InputRequired,
    Length
)
from app import db
from app.models import ScreeningQuestion

class ScreeningQuestionForm(Form):
    question = StringField(
        validators = [InputRequired(), Length(1, 256)])
    submit = SubmitField()
