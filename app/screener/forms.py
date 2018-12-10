from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import Length
from wtforms.widgets import TextArea

from .. import db
from app.models import Role, User

class EditScreenerInfoForm(Form):
    location = StringField(
        'Location')
    bio = TextAreaField(
        'Bio', render_kw={"rows": 4})
    languages = StringField(
        'Languages Spoken')
    immigrant_experience = TextAreaField(
        'Prior Experience with Immigrants', render_kw={"rows": 3})
    crime_experience = TextAreaField(
        'Prior Experience with Crime', render_kw={"rows": 3})

    submit = SubmitField('Update Profile')
