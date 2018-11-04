from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

from app import db
from app.models import DefaultChecklistItem


class DefaultChecklistItemForm(Form):
    title = StringField(
        validators=[InputRequired(),
                    Length(1, 64)])
    description = TextAreaField(
        validators=[InputRequired()])
    submit = SubmitField()
