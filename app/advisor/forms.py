from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import Length

from .. import db
from app.models import Role, User

class EditAdvisorInfoForm(Form):
    location = StringField(
        'Location')
    bio = TextAreaField(
        'Bio', render_kw={"rows": 4})
    languages = StringField(
        'Languages Spoken')
    law_experience = TextAreaField(
        'Law Experience', render_kw={"rows": 3})
    clemency_familiarity = TextAreaField(
        'Familiarity with Clemency Laws', render_kw={"rows": 3})

    submit = SubmitField('Update Profile')
