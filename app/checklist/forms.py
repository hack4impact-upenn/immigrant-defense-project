# Add new checklist item form
from flask_wtf import Form
from wtforms.fields import (
    StringField,
    SubmitField,
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
    description = StringField(
        'New Checklist Item Description',
        validators=[InputRequired(),
                    Length(1, 64)])
    submit = SubmitField('Add Checklist Item')


# Edit checklist item form
