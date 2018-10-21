from flask_wtf import Form
from wtforms.fields import (
    StringField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import (
    InputRequired,
    Length,
)
from app import db
from app.models import ChecklistItem


class NewChecklistItemForm(Form):
    title = StringField(
        'New Checklist Item',
        validators=[InputRequired(),
                    Length(1, 64)])
    description = TextAreaField(
        'New Checklist Item Description',
        validators=[InputRequired()])
    submit = SubmitField('Add Checklist Item')


class EditChecklistItemForm(Form):
    title = StringField(
        'Edit Checklist item title',
        validators=[InputRequired(),
                    Length(1, 64)])
    description = TextAreaField(
        'Edit Checklist item description',
        validators=[InputRequired()])
    submit = SubmitField('Edit Checklist Item')
